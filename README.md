# Learning Optimiser

```mermaid
flowchart TD;
  Embeddings[embed vocabulary]:::largeNode --> Cluster[cluster embeddings]:::largeNode;
  Cluster --> Sample[sample items from clusters]:::largeNode;

  classDef largeNode maxwidth: 20px
```
