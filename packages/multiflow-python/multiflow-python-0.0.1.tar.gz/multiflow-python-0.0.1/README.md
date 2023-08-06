# multiflow

Installation:

```bash
pip install multiflow-python
```

Usage instructions:

```python
import multiflow

workflow_id: str = ...

# assumes MULTIFLOW_API_KEY is set as an environment variable
w = multiflow.Workflow(workflow_id)

# get the type signature of the workflow
sig = w.type_signature()

# run the workflow
result = w.run(...)

print(result["outputs"])
```
