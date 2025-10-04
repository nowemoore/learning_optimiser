# Learning Optimiser

```mermaid
flowchart TD;
  Embeddings[embed vocabulary]:::largeNode --> Cluster[cluster embeddings]:::largeNode;
  Cluster --> Sample[sample items from clusters]:::largeNode;
  Sample -->

  classDef largeNode padding:20px,font-size:18px
```
