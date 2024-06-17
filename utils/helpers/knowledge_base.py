from langchain.retrievers import (ContextualCompressionRetriever,
                                  MergerRetriever)
from langchain.retrievers.document_compressors import \
    DocumentCompressorPipeline
from langchain_community.document_transformers import (
    EmbeddingsClusteringFilter, EmbeddingsRedundantFilter, LongContextReorder)

from utils.embeddings import instruct_embeddings
from utils.retrievers import custom_retriever, wiki_retriever

lotr = MergerRetriever(retrievers=[custom_retriever])


filter = EmbeddingsRedundantFilter(embeddings=instruct_embeddings)
pipeline = DocumentCompressorPipeline(transformers=[filter])
compression_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline, base_retriever=lotr
)

# This filter will divide the documents vectors into clusters or "centers" of meaning.
# Then it will pick the closest document to that center for the final results.
# By default the result document will be ordered/grouped by clusters.
filter_ordered_cluster = EmbeddingsClusteringFilter(
    embeddings=instruct_embeddings,
    num_clusters=10,
    num_closest=1,
)

# If you want the final document to be ordered by the original retriever scores
# you need to add the "sorted" parameter.
filter_ordered_by_retriever = EmbeddingsClusteringFilter(
    embeddings=instruct_embeddings,
    num_clusters=10,
    num_closest=1,
    sorted=True,
)

pipeline = DocumentCompressorPipeline(transformers=[filter_ordered_by_retriever])
compression_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline, base_retriever=lotr
)

# You can use an additional document transformer to reorder documents after removing redundancy.
filter = EmbeddingsRedundantFilter(embeddings=instruct_embeddings)
reordering = LongContextReorder()
pipeline = DocumentCompressorPipeline(transformers=[filter, reordering])
compression_retriever_reordered = ContextualCompressionRetriever(
    base_compressor=pipeline, base_retriever=lotr
)
