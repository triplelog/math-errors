// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "sandboxed_api/rpcchannel.h"

#include <glog/logging.h>
#include "absl/strings/str_cat.h"
#include "absl/synchronization/mutex.h"
#include "sandboxed_api/call.h"
#include "sandboxed_api/sandbox2/comms.h"
#include "sandboxed_api/util/status_macros.h"

namespace sapi {

absl::Status RPCChannel::Call(const FuncCall& call, uint32_t tag, FuncRet* ret,
                              v::Type exp_type) {
  absl::MutexLock lock(&mutex_);
  if (!comms_->SendTLV(tag, sizeof(call),
                       reinterpret_cast<const uint8_t*>(&call))) {
    return absl::UnavailableError("Sending TLV value failed");
  }
  SAPI_ASSIGN_OR_RETURN(auto fret, Return(exp_type));
  *ret = fret;
  return absl::OkStatus();
}

sapi::StatusOr<FuncRet> RPCChannel::Return(v::Type exp_type) {
  uint32_t tag;
  uint64_t len;
  FuncRet ret;
  if (!comms_->RecvTLV(&tag, &len, &ret, sizeof(ret))) {
    return absl::UnavailableError("Receiving TLV value failed");
  }
  if (tag != comms::kMsgReturn) {
    LOG(ERROR) << "tag != comms::kMsgReturn (" << absl::StrCat(absl::Hex(tag))
               << " != " << absl::StrCat(absl::Hex(comms::kMsgReturn)) << ")";
    return absl::UnavailableError("Received TLV has incorrect tag");
  }
  if (len != sizeof(FuncRet)) {
    LOG(ERROR) << "len != sizeof(FuncReturn) (" << len
               << " != " << sizeof(FuncRet) << ")";
    return absl::UnavailableError("Received TLV has incorrect length");
  }
  if (ret.ret_type != exp_type) {
    LOG(ERROR) << "FuncRet->type != exp_type (" << ret.ret_type
               << " != " << exp_type << ")";
    return absl::UnavailableError("Received TLV has incorrect return type");
  }
  if (!ret.success) {
    LOG(ERROR) << "FuncRet->success == false";
    return absl::UnavailableError("Function call failed");
  }
  return ret;
}

absl::Status RPCChannel::Allocate(size_t size, void** addr) {
  absl::MutexLock lock(&mutex_);
  uint64_t sz = size;
  if (!comms_->SendTLV(comms::kMsgAllocate, sizeof(sz),
                       reinterpret_cast<uint8_t*>(&sz))) {
    return absl::UnavailableError("Sending TLV value failed");
  }

  SAPI_ASSIGN_OR_RETURN(auto fret, Return(v::Type::kPointer));
  *addr = reinterpret_cast<void*>(fret.int_val);
  return absl::OkStatus();
}

absl::Status RPCChannel::Reallocate(void* old_addr, size_t size,
                                    void** new_addr) {
  absl::MutexLock lock(&mutex_);
  comms::ReallocRequest req;
  req.old_addr = reinterpret_cast<uint64_t>(old_addr);
  req.size = size;

  if (!comms_->SendTLV(comms::kMsgReallocate, sizeof(comms::ReallocRequest),
                       reinterpret_cast<uint8_t*>(&req))) {
    return absl::UnavailableError("Sending TLV value failed");
  }

  auto fret_or = Return(v::Type::kPointer);
  if (!fret_or.ok()) {
    *new_addr = nullptr;
    return absl::UnavailableError(
        absl::StrCat("Reallocate() failed on the remote side: ",
                     fret_or.status().message()));
  }
  auto fret = std::move(fret_or).ValueOrDie();

  *new_addr = reinterpret_cast<void*>(fret.int_val);
  return absl::OkStatus();
}

absl::Status RPCChannel::Free(void* addr) {
  absl::MutexLock lock(&mutex_);
  uint64_t remote = reinterpret_cast<uint64_t>(addr);
  if (!comms_->SendTLV(comms::kMsgFree, sizeof(remote),
                       reinterpret_cast<uint8_t*>(&remote))) {
    return absl::UnavailableError("Sending TLV value failed");
  }

  SAPI_ASSIGN_OR_RETURN(auto fret, Return(v::Type::kVoid));
  if (!fret.success) {
    return absl::UnavailableError("Free() failed on the remote side");
  }
  return absl::OkStatus();
}

absl::Status RPCChannel::Symbol(const char* symname, void** addr) {
  absl::MutexLock lock(&mutex_);
  if (!comms_->SendTLV(comms::kMsgSymbol, strlen(symname) + 1,
                       reinterpret_cast<const uint8_t*>(symname))) {
    return absl::UnavailableError("Sending TLV value failed");
  }

  SAPI_ASSIGN_OR_RETURN(auto fret, Return(v::Type::kPointer));
  *addr = reinterpret_cast<void*>(fret.int_val);
  return absl::OkStatus();
}

absl::Status RPCChannel::Exit() {
  absl::MutexLock lock(&mutex_);
  if (comms_->IsTerminated()) {
    VLOG(2) << "Comms channel already terminated";
    return absl::OkStatus();
  }

  // Try the RPC exit sequence. But, the only thing that matters as a success
  // indicator is whether the Comms channel had been closed
  bool unused = true;
  comms_->SendTLV(comms::kMsgExit, sizeof(unused),
                  reinterpret_cast<uint8_t*>(&unused));
  comms_->RecvBool(&unused);

  if (!comms_->IsTerminated()) {
    LOG(ERROR) << "Comms channel not terminated in Exit()";
    // TODO(hamacher): Better error code
    return absl::FailedPreconditionError(
        "Comms channel not terminated in Exit()");
  }

  return absl::OkStatus();
}

absl::Status RPCChannel::SendFD(int local_fd, int* remote_fd) {
  absl::MutexLock lock(&mutex_);
  bool unused = true;
  if (!comms_->SendTLV(comms::kMsgSendFd, sizeof(unused),
                       reinterpret_cast<uint8_t*>(&unused))) {
    return absl::UnavailableError("Sending TLV value failed");
  }
  if (!comms_->SendFD(local_fd)) {
    return absl::UnavailableError("Sending FD failed");
  }

  SAPI_ASSIGN_OR_RETURN(auto fret, Return(v::Type::kInt));
  if (!fret.success) {
    return absl::UnavailableError("SendFD failed on the remote side");
  }
  *remote_fd = fret.int_val;
  return absl::OkStatus();
}

absl::Status RPCChannel::RecvFD(int remote_fd, int* local_fd) {
  absl::MutexLock lock(&mutex_);
  if (!comms_->SendTLV(comms::kMsgRecvFd, sizeof(remote_fd),
                       reinterpret_cast<uint8_t*>(&remote_fd))) {
    return absl::UnavailableError("Sending TLV value failed");
  }

  if (!comms_->RecvFD(local_fd)) {
    return absl::UnavailableError("Receving FD failed");
  }

  SAPI_ASSIGN_OR_RETURN(auto fret, Return(v::Type::kVoid));
  if (!fret.success) {
    return absl::UnavailableError("RecvFD failed on the remote side");
  }
  return absl::OkStatus();
}

absl::Status RPCChannel::Close(int remote_fd) {
  absl::MutexLock lock(&mutex_);
  if (!comms_->SendTLV(comms::kMsgClose, sizeof(remote_fd),
                       reinterpret_cast<uint8_t*>(&remote_fd))) {
    return absl::UnavailableError("Sending TLV value failed");
  }

  SAPI_ASSIGN_OR_RETURN(auto fret, Return(v::Type::kVoid));
  if (!fret.success) {
    return absl::UnavailableError("Close() failed on the remote side");
  }
  return absl::OkStatus();
}

sapi::StatusOr<uint64_t> RPCChannel::Strlen(void* str) {
  absl::MutexLock lock(&mutex_);
  if (!comms_->SendTLV(comms::kMsgStrlen, sizeof(str),
                       reinterpret_cast<uint8_t*>(&str))) {
    return absl::UnavailableError("Sending TLV value failed");
  }

  SAPI_ASSIGN_OR_RETURN(auto fret, Return(v::Type::kInt));
  if (!fret.success) {
    return absl::UnavailableError("Close() failed on the remote side");
  }
  return fret.int_val;
}

}  // namespace sapi
