"""Profile Migration utility — converted from the original utility-a.py."""

from utilities_web import FileInput, create_app

app = create_app(
    title="Advanced Profile Migration Utility",
    inputs=[
        FileInput("application.properties"),
        FileInput("app_tuning.properties"),
        FileInput("log4j2.xml"),
        FileInput("keystoreFile.jceks"),
        FileInput("solutionDatesCounts.csv", accept=".csv"),
        FileInput("customUserDatesCounts.csv", accept=".csv"),
        FileInput("analyticsDatesCounts.csv", accept=".csv"),
    ],
    process_command=[
        "python",
        "run_migration.py",
        "{application.properties}",
        "{app_tuning.properties}",
        "{log4j2.xml}",
        "{keystoreFile.jceks}",
        "{solutionDatesCounts.csv}",
        "{customUserDatesCounts.csv}",
        "{analyticsDatesCounts.csv}",
    ],
    example_folder="example_files",
    enable_examples=True,
    success_message="Migration completed successfully!",
)

if __name__ == "__main__":
    app.run(debug=True)
