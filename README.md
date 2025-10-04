# Learning Optimiser

```mermaid
flowchart TD;
  Embeddings[embed vocabulary]:::largeNode --> Cluster[cluster embeddings]:::largeNode;
  Cluster --> Sample[sample items from clusters]::::::largeNode;

  classDef largeNode max-width: 20px
```
