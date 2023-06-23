import logging
from sys import stdout

import jenkins_source
import http_source
import github_source


download_dir = './'


root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


citizens_jenkins_url = 'https://ci.citizensnpcs.co'
citizens_job_name = 'Citizens2'
jenkins_source.get_newest_build(download_dir, citizens_jenkins_url, citizens_job_name)
citizens_sentinel_job_name = 'Sentinel'
jenkins_source.get_newest_build(download_dir, citizens_jenkins_url, citizens_sentinel_job_name)

fawe_jenkins_url = 'https://ci.athion.net'
fawe_job_name = 'FastAsyncWorldEdit'
jenkins_source.get_newest_build(download_dir, fawe_jenkins_url, fawe_job_name, '.*Bukkit.*')

# multiverse_jenkins_url = 'https://ci.onarandombox.com'
# multiverse_core_job_name = 'Multiverse-Core'
# jenkins_source.get_newest_build(download_dir, multiverse_jenkins_url, multiverse_core_job_name, '.*SNAPSHOT.jar')
# multiverse_portals_job_name = 'Multiverse-Portals'
# jenkins_source.get_newest_build(download_dir, multiverse_jenkins_url, multiverse_portals_job_name, '.*SNAPSHOT.jar')
# multiverse_inventories_job_name = 'Multiverse-Inventories'
# jenkins_source.get_newest_build(download_dir, multiverse_jenkins_url, multiverse_inventories_job_name, '.*SNAPSHOT.jar')

# todo: worldguard 1.20 support is currently in beta and this file doesnt point
#  to the beta nor is there any way to access the latest beta
# worldguard_bukkit_latest_url = 'https://dev.bukkit.org/projects/worldguard/files/latest'
# worldguard_file = 'worldguard.jar'
# http_source.get_newest_build(download_dir, worldguard_file, worldguard_bukkit_latest_url)

multiverse_owner = 'Multiverse'
multiverse_core_repo = 'Multiverse-Core'
github_source.get_newest_build(download_dir, multiverse_owner, multiverse_core_repo)
multiverse_inventories_repo = 'Multiverse-Inventories'
github_source.get_newest_build(download_dir, multiverse_owner, multiverse_inventories_repo)
multiverse_portals_repo = 'Multiverse-Portals'
github_source.get_newest_build(download_dir, multiverse_owner, multiverse_portals_repo)