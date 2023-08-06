/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace xla_cpu {
class AllReduceOp;
} // namespace xla_cpu
} // namespace mlir
namespace mlir {
namespace xla_cpu {
class AllToAllOp;
} // namespace xla_cpu
} // namespace mlir
namespace mlir {
namespace xla_cpu {
class CollectivePermuteOp;
} // namespace xla_cpu
} // namespace mlir
namespace mlir {
namespace xla_cpu {
class PartitionIdOp;
} // namespace xla_cpu
} // namespace mlir
namespace mlir {
namespace xla_cpu {
class ReplicaIdOp;
} // namespace xla_cpu
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace xla_cpu {

//===----------------------------------------------------------------------===//
// ::mlir::xla_cpu::AllReduceOp declarations
//===----------------------------------------------------------------------===//

class AllReduceOpAdaptor {
public:
  AllReduceOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  AllReduceOpAdaptor(AllReduceOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getOperand();
  ::mlir::ValueRange getDsts();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::DenseIntElementsAttr getReplicaGroupsAttr();
  ::mlir::DenseIntElementsAttr getReplicaGroups();
  ::mlir::IntegerAttr getChannelHandleAttr();
  uint64_t getChannelHandle();
  ::mlir::IntegerAttr getUseGlobalDeviceIdsAttr();
  uint32_t getUseGlobalDeviceIds();
  ::mlir::IntegerAttr getReductionKindAttr();
  ::llvm::APInt getReductionKind();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class AllReduceOp : public ::mlir::Op<AllReduceOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants, ::mlir::OpTrait::SameOperandsElementType, ::mlir::bufferization::BufferizableOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = AllReduceOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("channel_handle"), ::llvm::StringRef("reduction_kind"), ::llvm::StringRef("replica_groups"), ::llvm::StringRef("use_global_device_ids")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getChannelHandleAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getChannelHandleAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getReductionKindAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getReductionKindAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getReplicaGroupsAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getReplicaGroupsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getUseGlobalDeviceIdsAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getUseGlobalDeviceIdsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("xla_cpu.all_reduce");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getOperand();
  ::mlir::Operation::operand_range getDsts();
  ::mlir::MutableOperandRange getOperandMutable();
  ::mlir::MutableOperandRange getDstsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::DenseIntElementsAttr getReplicaGroupsAttr();
  ::mlir::DenseIntElementsAttr getReplicaGroups();
  ::mlir::IntegerAttr getChannelHandleAttr();
  uint64_t getChannelHandle();
  ::mlir::IntegerAttr getUseGlobalDeviceIdsAttr();
  uint32_t getUseGlobalDeviceIds();
  ::mlir::IntegerAttr getReductionKindAttr();
  ::llvm::APInt getReductionKind();
  void setReplicaGroupsAttr(::mlir::DenseIntElementsAttr attr);
  void setChannelHandleAttr(::mlir::IntegerAttr attr);
  void setChannelHandle(uint64_t attrValue);
  void setUseGlobalDeviceIdsAttr(::mlir::IntegerAttr attr);
  void setUseGlobalDeviceIds(uint32_t attrValue);
  void setReductionKindAttr(::mlir::IntegerAttr attr);
  void setReductionKind(::llvm::APInt attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::ValueRange operand, ::mlir::ValueRange dsts, ::mlir::DenseIntElementsAttr replica_groups, ::mlir::IntegerAttr channel_handle, ::mlir::IntegerAttr use_global_device_ids, ::mlir::IntegerAttr reduction_kind);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::ValueRange operand, ::mlir::ValueRange dsts, ::mlir::DenseIntElementsAttr replica_groups, uint64_t channel_handle, uint32_t use_global_device_ids, ::llvm::APInt reduction_kind);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 4 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
  // Declarations for BufferizableOpInterface:
  bool bufferizesToMemoryRead(OpOperand &opOperand,
      const bufferization::AnalysisState &state);
  bool bufferizesToMemoryWrite(OpOperand &opOperand,
      const bufferization::AnalysisState &state);
  SmallVector<OpResult> getAliasingOpResult(
      OpOperand &opOperand, const bufferization::AnalysisState &state);
  LogicalResult bufferize(RewriterBase &rewriter,
      const bufferization::BufferizationOptions &options);
  bufferization::BufferRelation bufferRelation(OpResult opResult,
      const bufferization::AnalysisState &state);
};
} // namespace xla_cpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xla_cpu::AllReduceOp)

namespace mlir {
namespace xla_cpu {

//===----------------------------------------------------------------------===//
// ::mlir::xla_cpu::AllToAllOp declarations
//===----------------------------------------------------------------------===//

class AllToAllOpAdaptor {
public:
  AllToAllOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  AllToAllOpAdaptor(AllToAllOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getOperand();
  ::mlir::Value getDst();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::DenseIntElementsAttr getReplicaGroupsAttr();
  ::mlir::DenseIntElementsAttr getReplicaGroups();
  ::mlir::IntegerAttr getSplitDimensionAttr();
  uint64_t getSplitDimension();
  ::mlir::IntegerAttr getConcatDimensionAttr();
  uint64_t getConcatDimension();
  ::mlir::IntegerAttr getSplitCountAttr();
  uint64_t getSplitCount();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class AllToAllOp : public ::mlir::Op<AllToAllOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<2>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::bufferization::BufferizableOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = AllToAllOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("concat_dimension"), ::llvm::StringRef("replica_groups"), ::llvm::StringRef("split_count"), ::llvm::StringRef("split_dimension")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getConcatDimensionAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getConcatDimensionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getReplicaGroupsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getReplicaGroupsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getSplitCountAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getSplitCountAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr getSplitDimensionAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getSplitDimensionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("xla_cpu.all_to_all");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::ShapedType> getOperand();
  ::mlir::TypedValue<::mlir::ShapedType> getDst();
  ::mlir::MutableOperandRange getOperandMutable();
  ::mlir::MutableOperandRange getDstMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::DenseIntElementsAttr getReplicaGroupsAttr();
  ::mlir::DenseIntElementsAttr getReplicaGroups();
  ::mlir::IntegerAttr getSplitDimensionAttr();
  uint64_t getSplitDimension();
  ::mlir::IntegerAttr getConcatDimensionAttr();
  uint64_t getConcatDimension();
  ::mlir::IntegerAttr getSplitCountAttr();
  uint64_t getSplitCount();
  void setReplicaGroupsAttr(::mlir::DenseIntElementsAttr attr);
  void setSplitDimensionAttr(::mlir::IntegerAttr attr);
  void setSplitDimension(uint64_t attrValue);
  void setConcatDimensionAttr(::mlir::IntegerAttr attr);
  void setConcatDimension(uint64_t attrValue);
  void setSplitCountAttr(::mlir::IntegerAttr attr);
  void setSplitCount(uint64_t attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::Value operand, ::mlir::Value dst, ::mlir::DenseIntElementsAttr replica_groups, ::mlir::IntegerAttr split_dimension, ::mlir::IntegerAttr concat_dimension, ::mlir::IntegerAttr split_count);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::Value operand, ::mlir::Value dst, ::mlir::DenseIntElementsAttr replica_groups, uint64_t split_dimension, uint64_t concat_dimension, uint64_t split_count);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 4 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
  // Declarations for BufferizableOpInterface:
  bool bufferizesToMemoryRead(OpOperand &opOperand,
      const bufferization::AnalysisState &state) {
    return opOperand.getOperandNumber() == 0;
  }
  bool bufferizesToMemoryWrite(OpOperand &opOperand,
      const bufferization::AnalysisState &state) {
    return opOperand.getOperandNumber() == 1;
  }
  SmallVector<OpResult> getAliasingOpResult(
      OpOperand &opOperand, const bufferization::AnalysisState &state) {
    if (opOperand.getOperandNumber() == 0) return {};
    return {getOperation()->getOpResult(0)};
  }
  LogicalResult bufferize(RewriterBase &rewriter,
      const bufferization::BufferizationOptions &options);
  bufferization::BufferRelation bufferRelation(OpResult opResult,
      const bufferization::AnalysisState &state) {
    return bufferization::BufferRelation::Equivalent;
  }
};
} // namespace xla_cpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xla_cpu::AllToAllOp)

namespace mlir {
namespace xla_cpu {

//===----------------------------------------------------------------------===//
// ::mlir::xla_cpu::CollectivePermuteOp declarations
//===----------------------------------------------------------------------===//

class CollectivePermuteOpAdaptor {
public:
  CollectivePermuteOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  CollectivePermuteOpAdaptor(CollectivePermuteOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getOperand();
  ::mlir::Value getDst();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::DenseIntElementsAttr getSourceTargetPairsAttr();
  ::mlir::DenseIntElementsAttr getSourceTargetPairs();
  ::mlir::IntegerAttr getChannelHandleAttr();
  uint64_t getChannelHandle();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class CollectivePermuteOp : public ::mlir::Op<CollectivePermuteOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<2>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::bufferization::BufferizableOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = CollectivePermuteOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("channel_handle"), ::llvm::StringRef("source_target_pairs")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getChannelHandleAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getChannelHandleAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getSourceTargetPairsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getSourceTargetPairsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("xla_cpu.collective_permute");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::ShapedType> getOperand();
  ::mlir::TypedValue<::mlir::ShapedType> getDst();
  ::mlir::MutableOperandRange getOperandMutable();
  ::mlir::MutableOperandRange getDstMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::DenseIntElementsAttr getSourceTargetPairsAttr();
  ::mlir::DenseIntElementsAttr getSourceTargetPairs();
  ::mlir::IntegerAttr getChannelHandleAttr();
  uint64_t getChannelHandle();
  void setSourceTargetPairsAttr(::mlir::DenseIntElementsAttr attr);
  void setChannelHandleAttr(::mlir::IntegerAttr attr);
  void setChannelHandle(uint64_t attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::Value operand, ::mlir::Value dst, ::mlir::DenseIntElementsAttr source_target_pairs, ::mlir::IntegerAttr channel_handle);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultType0, ::mlir::Value operand, ::mlir::Value dst, ::mlir::DenseIntElementsAttr source_target_pairs, uint64_t channel_handle);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
  // Declarations for BufferizableOpInterface:
  bool bufferizesToMemoryRead(OpOperand &opOperand,
      const bufferization::AnalysisState &state) {
    return opOperand.getOperandNumber() == 0;
  }
  bool bufferizesToMemoryWrite(OpOperand   &opOperand,
      const bufferization::AnalysisState &state) {
    return opOperand.getOperandNumber() == 1;
  }
  SmallVector<OpResult> getAliasingOpResult(
      OpOperand &opOperand, const bufferization::AnalysisState &state) {
    if (opOperand.getOperandNumber() == 0) return {};
    return {getOperation()->getOpResult(0)};
  }
  LogicalResult bufferize(RewriterBase &rewriter,
      const bufferization::BufferizationOptions &options);
  bufferization::BufferRelation bufferRelation(OpResult opResult,
      const bufferization::AnalysisState &state) {
    return bufferization::BufferRelation::Equivalent;
  }
};
} // namespace xla_cpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xla_cpu::CollectivePermuteOp)

namespace mlir {
namespace xla_cpu {

//===----------------------------------------------------------------------===//
// ::mlir::xla_cpu::PartitionIdOp declarations
//===----------------------------------------------------------------------===//

class PartitionIdOpAdaptor {
public:
  PartitionIdOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  PartitionIdOpAdaptor(PartitionIdOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class PartitionIdOp : public ::mlir::Op<PartitionIdOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::IntegerType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, ::mlir::InferTypeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = PartitionIdOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("xla_cpu.partition_id");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type resultType0);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::LogicalResult inferReturnTypes(::mlir::MLIRContext *context, ::llvm::Optional<::mlir::Location> location, ::mlir::ValueRange operands, ::mlir::DictionaryAttr attributes, ::mlir::RegionRange regions, ::llvm::SmallVectorImpl<::mlir::Type>&inferredReturnTypes);
public:
};
} // namespace xla_cpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xla_cpu::PartitionIdOp)

namespace mlir {
namespace xla_cpu {

//===----------------------------------------------------------------------===//
// ::mlir::xla_cpu::ReplicaIdOp declarations
//===----------------------------------------------------------------------===//

class ReplicaIdOpAdaptor {
public:
  ReplicaIdOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ReplicaIdOpAdaptor(ReplicaIdOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ReplicaIdOp : public ::mlir::Op<ReplicaIdOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::IntegerType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::ZeroOperands, ::mlir::OpTrait::OpInvariants, ::mlir::InferTypeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ReplicaIdOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("xla_cpu.replica_id");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type resultType0);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::LogicalResult inferReturnTypes(::mlir::MLIRContext *context, ::llvm::Optional<::mlir::Location> location, ::mlir::ValueRange operands, ::mlir::DictionaryAttr attributes, ::mlir::RegionRange regions, ::llvm::SmallVectorImpl<::mlir::Type>&inferredReturnTypes);
public:
};
} // namespace xla_cpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xla_cpu::ReplicaIdOp)


#endif  // GET_OP_CLASSES

