from kfp import dsl

@dsl.pipeline(
    name="simple-ml-pipeline",
    description="Demo Vertex AI pipeline"
)
def simple_pipeline():
    @dsl.component
    def log_step():
        print("Hello from Vertex AI Pipeline!")

    log_step()
