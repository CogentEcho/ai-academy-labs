# core/safety.py
from pathlib import Path
import shutil
import git
from datetime import datetime
import logging

class SafetyManager:
    """Core safety mechanisms for repository operations."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.backup_dir = repo_path.parent / "backups"
        self.logger = logging.getLogger(__name__)
        
    def create_backup(self) -> Path:
        """Create timestamped backup of repository."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        
        self.backup_dir.mkdir(exist_ok=True)
        shutil.copytree(self.repo_path, backup_path)
        return backup_path
    
    def validate_git_state(self) -> bool:
        """Check if git repository is in a clean state."""
        repo = git.Repo(self.repo_path)
        return not repo.is_dirty()
    
    def safe_operation(self, operation):
        """Decorator to ensure operations are performed safely."""
        def wrapper(*args, **kwargs):
            if not self.validate_git_state():
                raise ValueError("Repository has uncommitted changes")
            
            backup_path = self.create_backup()
            try:
                result = operation(*args, **kwargs)
                return result
            except Exception as e:
                self.logger.error(f"Operation failed: {str(e)}")
                self.restore_from_backup(backup_path)
                raise
        return wrapper

# prompts/catalog.py
from dataclasses import dataclass
from typing import Dict, List
import yaml

@dataclass
class PromptTemplate:
    name: str
    template: str
    metadata: Dict
    usage_count: int = 0
    
class PromptCatalog:
    """Manages and tracks prompt templates."""
    
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load prompt templates from YAML files."""
        for template_file in self.template_dir.glob("*.yaml"):
            with open(template_file) as f:
                template_data = yaml.safe_load(f)
                self.templates[template_data["name"]] = PromptTemplate(
                    name=template_data["name"],
                    template=template_data["template"],
                    metadata=template_data.get("metadata", {})
                )
    
    def get_prompt(self, name: str, **kwargs) -> str:
        """Get formatted prompt template."""
        if name not in self.templates:
            raise KeyError(f"Template {name} not found")
        
        template = self.templates[name]
        template.usage_count += 1
        return template.template.format(**kwargs)

# analyzers/content.py
from pathlib import Path
from typing import Dict, List
import re

class ContentAnalyzer:
    """Analyzes repository content for quality and consistency."""
    
    def __init__(self):
        self.patterns = {
            'broken_links': r'\[([^\]]+)\]\(([^\)]+)\)',
            'todo_markers': r'TODO|FIXME',
            'empty_sections': r'#.*\n\s*\n#'
        }
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single file for issues."""
        with open(file_path) as f:
            content = f.read()
            
        issues = {
            'broken_links': [],
            'todos': [],
            'empty_sections': []
        }
        
        # Check for broken links
        for match in re.finditer(self.patterns['broken_links'], content):
            link_text, link_target = match.groups()
            if not self._validate_link(link_target):
                issues['broken_links'].append(link_target)
        
        # Find TODOs
        for match in re.finditer(self.patterns['todo_markers'], content):
            issues['todos'].append(match.group(0))
            
        return issues

# feedback/collector.py
from dataclasses import dataclass
from typing import List, Dict
import json
from pathlib import Path

@dataclass
class Feedback:
    type: str
    message: str
    severity: str
    location: str
    
class FeedbackCollector:
    """Collects and manages system feedback."""
    
    def __init__(self, feedback_file: Path):
        self.feedback_file = feedback_file
        self.feedback: List[Feedback] = []
        self._load_feedback()
    
    def _load_feedback(self):
        """Load existing feedback from file."""
        if self.feedback_file.exists():
            with open(self.feedback_file) as f:
                data = json.load(f)
                self.feedback = [Feedback(**item) for item in data]
    
    def add_feedback(self, feedback: Feedback):
        """Add new feedback and save."""
        self.feedback.append(feedback)
        self._save_feedback()
    
    def _save_feedback(self):
        """Save feedback to file."""
        with open(self.feedback_file, 'w') as f:
            json.dump([vars(f) for f in self.feedback], f, indent=2)

# tests/test_safety.py
import pytest
from pathlib import Path
from core.safety import SafetyManager

def test_safety_manager_backup():
    """Test backup creation and verification."""
    repo_path = Path("test_repo")
    safety = SafetyManager(repo_path)
    
    # Create test repository
    repo_path.mkdir(exist_ok=True)
    (repo_path / "test.txt").write_text("test content")
    
    # Test backup creation
    backup_path = safety.create_backup()
    assert backup_path.exists()
    assert (backup_path / "test.txt").read_text() == "test content"

def test_git_state_validation():
    """Test git state validation."""
    repo_path = Path("test_repo")
    safety = SafetyManager(repo_path)
    
    # Test clean state
    assert safety.validate_git_state()
    
    # Test dirty state
    (repo_path / "new_file.txt").write_text("new content")
    assert not safety.validate_git_state()

# main.py
import asyncio
from pathlib import Path
from core.safety import SafetyManager
from prompts.catalog import PromptCatalog
from analyzers.content import ContentAnalyzer
from feedback.collector import FeedbackCollector

async def main():
    """Main entry point for repository management."""
    repo_path = Path("ai-academy-labs")
    
    # Initialize components
    safety = SafetyManager(repo_path)
    prompts = PromptCatalog(repo_path / "prompts" / "templates")
    analyzer = ContentAnalyzer()
    feedback = FeedbackCollector(repo_path / "feedback" / "feedback.json")
    
    # Ensure safe state
    if not safety.validate_git_state():
        print("Repository has uncommitted changes. Please commit or stash them.")
        return
    
    # Create backup
    backup_path = safety.create_backup()
    print(f"Backup created at: {backup_path}")
    
    # Analyze repository
    issues = {}
    for md_file in repo_path.rglob("*.md"):
        issues[md_file] = analyzer.analyze_file(md_file)
    
    # Report issues
    for file, file_issues in issues.items():
        if any(file_issues.values()):
            feedback.add_feedback(Feedback(
                type="content_issues",
                message=f"Issues found in {file}",
                severity="warning",
                location=str(file)
            ))
    
    print("Analysis complete. Check feedback.json for details.")

if __name__ == "__main__":
    asyncio.run(main())
