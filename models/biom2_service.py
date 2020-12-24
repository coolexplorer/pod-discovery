
class Biom2Service:
    def __init__(self, id, name, major_version, minor_version, patch_version, url, type, environment, projects,
                 friendly_name, description, icon_url, source_link, docs_link):
        self.id = id
        self.name = name
        self.major_version = major_version
        self.minor_version = minor_version
        self.patch_version = patch_version
        self.url = url
        self.type = type
        self.environment = environment
        self.projects = projects
        self.friendly_name = friendly_name
        self.description = description
        self.icon_url = icon_url
        self.source_link = source_link
        self.docs_link = docs_link

    def __str__(self):
        return f'''------------ BioMetrics2 Service metadata ----------------
id: {self.id}, name: {self.name}, type: {self.type}, environment:{self.environment} 
projects: {self.projects}, friendlyName:{self.friendly_name}
majorVersion: {self.major_version}, minorVersion: {self.minor_version}, patchVersion: {self.patch_version}
url: {self.url}
description: {self.description}
sourceLink: {self.source_link}
docsLink: {self.docs_link}
iconLink: {self.icon_url}
'''
