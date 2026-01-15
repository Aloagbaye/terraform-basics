from kfp import compiler
from pipeline import simple_pipeline

compiler.Compiler().compile(
    pipeline_func=simple_pipeline,
    package_path="simple_pipeline.json"
)
