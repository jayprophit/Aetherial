"""
GitHub Deployment and Repository Management System
Comprehensive system for GitHub repository setup, CI/CD, and deployment automation
"""

import json
import uuid
import hashlib
import asyncio
import time
import os
import shutil
import subprocess
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import base64
import yaml

class RepositoryType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"

class LicenseType(Enum):
    MIT = "mit"
    APACHE_2_0 = "apache-2.0"
    GPL_V3 = "gpl-3.0"
    BSD_3_CLAUSE = "bsd-3-clause"
    PROPRIETARY = "proprietary"
    UNLICENSE = "unlicense"

class DeploymentTarget(Enum):
    GITHUB_PAGES = "github_pages"
    VERCEL = "vercel"
    NETLIFY = "netlify"
    HEROKU = "heroku"
    AWS = "aws"
    AZURE = "azure"
    GOOGLE_CLOUD = "google_cloud"
    DOCKER_HUB = "docker_hub"

class WorkflowTrigger(Enum):
    PUSH = "push"
    PULL_REQUEST = "pull_request"
    SCHEDULE = "schedule"
    WORKFLOW_DISPATCH = "workflow_dispatch"
    RELEASE = "release"

@dataclass
class RepositoryConfig:
    name: str
    description: str
    repository_type: RepositoryType
    license_type: LicenseType
    default_branch: str
    topics: List[str]
    homepage_url: Optional[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_downloads: bool
    auto_init: bool
    gitignore_template: Optional[str]
    license_template: Optional[str]

@dataclass
class WorkflowConfig:
    name: str
    triggers: List[WorkflowTrigger]
    jobs: List[Dict[str, Any]]
    environment_variables: Dict[str, str]
    secrets: List[str]
    schedule_cron: Optional[str]

@dataclass
class DeploymentConfig:
    target: DeploymentTarget
    environment: str
    build_command: str
    output_directory: str
    environment_variables: Dict[str, str]
    custom_domain: Optional[str]
    ssl_enabled: bool

class GitHubRepositoryManager:
    """GitHub repository management and setup"""
    
    def __init__(self):
        self.repositories = {}
        self.workflows = {}
        self.deployments = {}
        
        # Initialize templates
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize repository and workflow templates"""
        self.templates = {
            'gitignore': {
                'python': self._get_python_gitignore(),
                'node': self._get_node_gitignore(),
                'react': self._get_react_gitignore(),
                'general': self._get_general_gitignore()
            },
            'readme': {
                'unified_platform': self._get_unified_platform_readme(),
                'api': self._get_api_readme(),
                'frontend': self._get_frontend_readme(),
                'documentation': self._get_documentation_readme()
            },
            'workflows': {
                'ci_cd': self._get_ci_cd_workflow(),
                'deploy_pages': self._get_pages_deployment_workflow(),
                'docker_build': self._get_docker_workflow(),
                'security_scan': self._get_security_workflow()
            },
            'licenses': {
                LicenseType.MIT: self._get_mit_license(),
                LicenseType.APACHE_2_0: self._get_apache_license(),
                LicenseType.GPL_V3: self._get_gpl_license()
            }
        }
    
    def create_repository(self, config: RepositoryConfig) -> str:
        """Create new GitHub repository"""
        repo_id = str(uuid.uuid4())
        
        # Create repository structure
        repo_structure = {
            'id': repo_id,
            'name': config.name,
            'full_name': f"unified-platform/{config.name}",
            'description': config.description,
            'private': config.repository_type == RepositoryType.PRIVATE,
            'html_url': f"https://github.com/unified-platform/{config.name}",
            'clone_url': f"https://github.com/unified-platform/{config.name}.git",
            'ssh_url': f"git@github.com:unified-platform/{config.name}.git",
            'default_branch': config.default_branch,
            'topics': config.topics,
            'license': config.license_type.value if config.license_type != LicenseType.PROPRIETARY else None,
            'homepage': config.homepage_url,
            'has_issues': config.has_issues,
            'has_projects': config.has_projects,
            'has_wiki': config.has_wiki,
            'has_downloads': config.has_downloads,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'size': 0,
            'stargazers_count': 0,
            'watchers_count': 0,
            'forks_count': 0,
            'open_issues_count': 0
        }
        
        # Initialize repository files
        if config.auto_init:
            repo_structure['files'] = self._initialize_repository_files(config)
        
        self.repositories[repo_id] = repo_structure
        return repo_id
    
    def _initialize_repository_files(self, config: RepositoryConfig) -> Dict[str, str]:
        """Initialize repository with default files"""
        files = {}
        
        # README.md
        if config.name.startswith('unified-platform'):
            files['README.md'] = self.templates['readme']['unified_platform']
        else:
            files['README.md'] = self._generate_basic_readme(config)
        
        # .gitignore
        if config.gitignore_template:
            files['.gitignore'] = self.templates['gitignore'].get(
                config.gitignore_template, 
                self.templates['gitignore']['general']
            )
        
        # LICENSE
        if config.license_type != LicenseType.PROPRIETARY:
            files['LICENSE'] = self.templates['licenses'].get(
                config.license_type,
                self.templates['licenses'][LicenseType.MIT]
            )
        
        # CONTRIBUTING.md
        files['CONTRIBUTING.md'] = self._get_contributing_guidelines()
        
        # CODE_OF_CONDUCT.md
        files['CODE_OF_CONDUCT.md'] = self._get_code_of_conduct()
        
        # SECURITY.md
        files['SECURITY.md'] = self._get_security_policy()
        
        # .github/ISSUE_TEMPLATE/
        files['.github/ISSUE_TEMPLATE/bug_report.md'] = self._get_bug_report_template()
        files['.github/ISSUE_TEMPLATE/feature_request.md'] = self._get_feature_request_template()
        
        # .github/PULL_REQUEST_TEMPLATE.md
        files['.github/PULL_REQUEST_TEMPLATE.md'] = self._get_pr_template()
        
        return files
    
    def setup_ci_cd_workflow(self, repo_id: str, workflow_config: WorkflowConfig) -> str:
        """Setup CI/CD workflow for repository"""
        workflow_id = str(uuid.uuid4())
        
        if repo_id not in self.repositories:
            raise ValueError("Repository not found")
        
        # Generate workflow YAML
        workflow_yaml = self._generate_workflow_yaml(workflow_config)
        
        workflow = {
            'id': workflow_id,
            'repo_id': repo_id,
            'name': workflow_config.name,
            'file_path': f'.github/workflows/{workflow_config.name.lower().replace(" ", "_")}.yml',
            'content': workflow_yaml,
            'triggers': [trigger.value for trigger in workflow_config.triggers],
            'status': 'active',
            'created_at': datetime.now(),
            'last_run': None,
            'success_rate': 0.0,
            'total_runs': 0
        }
        
        self.workflows[workflow_id] = workflow
        
        # Add workflow file to repository
        repo = self.repositories[repo_id]
        if 'files' not in repo:
            repo['files'] = {}
        repo['files'][workflow['file_path']] = workflow_yaml
        
        return workflow_id
    
    def _generate_workflow_yaml(self, config: WorkflowConfig) -> str:
        """Generate GitHub Actions workflow YAML"""
        workflow = {
            'name': config.name,
            'on': {}
        }
        
        # Configure triggers
        for trigger in config.triggers:
            if trigger == WorkflowTrigger.PUSH:
                workflow['on']['push'] = {
                    'branches': ['main', 'develop'],
                    'paths-ignore': ['**.md', 'docs/**']
                }
            elif trigger == WorkflowTrigger.PULL_REQUEST:
                workflow['on']['pull_request'] = {
                    'branches': ['main', 'develop']
                }
            elif trigger == WorkflowTrigger.SCHEDULE:
                if config.schedule_cron:
                    workflow['on']['schedule'] = [{'cron': config.schedule_cron}]
            elif trigger == WorkflowTrigger.WORKFLOW_DISPATCH:
                workflow['on']['workflow_dispatch'] = {}
            elif trigger == WorkflowTrigger.RELEASE:
                workflow['on']['release'] = {'types': ['published']}
        
        # Add environment variables
        if config.environment_variables:
            workflow['env'] = config.environment_variables
        
        # Add jobs
        workflow['jobs'] = {}
        for job_config in config.jobs:
            job_name = job_config['name']
            workflow['jobs'][job_name] = {
                'runs-on': job_config.get('runs_on', 'ubuntu-latest'),
                'steps': job_config.get('steps', [])
            }
            
            # Add environment variables to job if specified
            if 'environment' in job_config:
                workflow['jobs'][job_name]['environment'] = job_config['environment']
        
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False)
    
    def setup_deployment(self, repo_id: str, deployment_config: DeploymentConfig) -> str:
        """Setup deployment configuration"""
        deployment_id = str(uuid.uuid4())
        
        if repo_id not in self.repositories:
            raise ValueError("Repository not found")
        
        deployment = {
            'id': deployment_id,
            'repo_id': repo_id,
            'target': deployment_config.target,
            'environment': deployment_config.environment,
            'build_command': deployment_config.build_command,
            'output_directory': deployment_config.output_directory,
            'environment_variables': deployment_config.environment_variables,
            'custom_domain': deployment_config.custom_domain,
            'ssl_enabled': deployment_config.ssl_enabled,
            'status': 'configured',
            'last_deployment': None,
            'deployment_url': None,
            'created_at': datetime.now()
        }
        
        # Generate deployment-specific files
        deployment_files = self._generate_deployment_files(deployment_config)
        
        # Add deployment files to repository
        repo = self.repositories[repo_id]
        if 'files' not in repo:
            repo['files'] = {}
        repo['files'].update(deployment_files)
        
        # Generate deployment URL
        deployment['deployment_url'] = self._generate_deployment_url(repo_id, deployment_config)
        
        self.deployments[deployment_id] = deployment
        return deployment_id
    
    def _generate_deployment_files(self, config: DeploymentConfig) -> Dict[str, str]:
        """Generate deployment-specific configuration files"""
        files = {}
        
        if config.target == DeploymentTarget.VERCEL:
            files['vercel.json'] = json.dumps({
                'version': 2,
                'builds': [
                    {
                        'src': 'package.json',
                        'use': '@vercel/node'
                    }
                ],
                'routes': [
                    {
                        'src': '/(.*)',
                        'dest': '/index.html'
                    }
                ],
                'env': config.environment_variables
            }, indent=2)
        
        elif config.target == DeploymentTarget.NETLIFY:
            files['netlify.toml'] = f"""
[build]
  command = "{config.build_command}"
  publish = "{config.output_directory}"

[build.environment]
{chr(10).join(f'  {k} = "{v}"' for k, v in config.environment_variables.items())}

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
        
        elif config.target == DeploymentTarget.HEROKU:
            files['Procfile'] = 'web: npm start'
            files['app.json'] = json.dumps({
                'name': 'Unified Platform',
                'description': 'Revolutionary unified platform',
                'repository': 'https://github.com/unified-platform/app',
                'keywords': ['unified', 'platform', 'business'],
                'env': {
                    key: {'description': f'Environment variable {key}'}
                    for key in config.environment_variables.keys()
                }
            }, indent=2)
        
        elif config.target == DeploymentTarget.DOCKER_HUB:
            files['Dockerfile'] = self._get_dockerfile_template()
            files['docker-compose.yml'] = self._get_docker_compose_template()
            files['.dockerignore'] = self._get_dockerignore_template()
        
        return files
    
    def _generate_deployment_url(self, repo_id: str, config: DeploymentConfig) -> str:
        """Generate deployment URL"""
        repo = self.repositories[repo_id]
        repo_name = repo['name']
        
        if config.custom_domain:
            return f"https://{config.custom_domain}"
        
        if config.target == DeploymentTarget.GITHUB_PAGES:
            return f"https://unified-platform.github.io/{repo_name}"
        elif config.target == DeploymentTarget.VERCEL:
            return f"https://{repo_name}-unified-platform.vercel.app"
        elif config.target == DeploymentTarget.NETLIFY:
            return f"https://{repo_name}-unified-platform.netlify.app"
        elif config.target == DeploymentTarget.HEROKU:
            return f"https://{repo_name}-unified-platform.herokuapp.com"
        else:
            return f"https://{repo_name}.unified-platform.com"
    
    def create_release(self, repo_id: str, version: str, release_notes: str) -> str:
        """Create GitHub release"""
        release_id = str(uuid.uuid4())
        
        if repo_id not in self.repositories:
            raise ValueError("Repository not found")
        
        release = {
            'id': release_id,
            'repo_id': repo_id,
            'tag_name': f'v{version}',
            'name': f'Release {version}',
            'body': release_notes,
            'draft': False,
            'prerelease': False,
            'created_at': datetime.now(),
            'published_at': datetime.now(),
            'assets': [],
            'download_count': 0
        }
        
        # Update repository
        repo = self.repositories[repo_id]
        if 'releases' not in repo:
            repo['releases'] = []
        repo['releases'].append(release)
        
        return release_id
    
    def get_repository_analytics(self, repo_id: str) -> Dict[str, Any]:
        """Get repository analytics and metrics"""
        if repo_id not in self.repositories:
            raise ValueError("Repository not found")
        
        repo = self.repositories[repo_id]
        
        # Calculate metrics
        total_commits = len(repo.get('commits', []))
        total_contributors = len(repo.get('contributors', []))
        total_releases = len(repo.get('releases', []))
        
        # Workflow metrics
        repo_workflows = [w for w in self.workflows.values() if w['repo_id'] == repo_id]
        total_workflows = len(repo_workflows)
        successful_runs = sum(w.get('successful_runs', 0) for w in repo_workflows)
        total_runs = sum(w.get('total_runs', 0) for w in repo_workflows)
       
(Content truncated due to size limit. Use line ranges to read in chunks)