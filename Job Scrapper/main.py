from indeed import get_jobs
from so import get_jobs as so_get_jobs
from save import save_to_file

so_jobs = so_get_jobs()
indeed_jobs = get_jobs()
jobs = so_jobs + indeed_jobs
save_to_file(jobs)