import os
import json
from oversight_agent import OversightAgent
from repository_manager import RepositoryManager
from cms_integrator import CMSIntegrator

def main():
    # Load the structure.js file
    with open("structure.js") as file:
        structure_data = file.read()

    # Parse the JavaScript object from the structure_data
    structure = json.loads(structure_data.split(" = ", 1)[1].strip().rstrip(";"))

    # Initialize the oversight agent
    oversight_agent = OversightAgent(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Initialize the repository manager
    repo_manager = RepositoryManager(oversight_agent)

    # Initialize the CMS integrator
    cms_integrator = CMSIntegrator(oversight_agent)

    # Execute the steps with oversight
    repo_manager.refine_repository_structure(structure["newStructure"])
    cms_integrator.integrate_cms(structure["cmsOptions"])

if __name__ == "__main__":
    main()