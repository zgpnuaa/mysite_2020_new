import time
import json
from django.shortcuts import render
from monitor import models

# Create your views here.


def show_procstat(request):
    servers = ['zhugaoping', ]
    procstat_ret = {}
    for server in servers:
        procstat_info = models.ProcstatInfo.objects.filter(host=server)
        procstat_exe = {}
        for row in procstat_info:
            temp_time = int(time.mktime(row.time.timetuple())) * 1000
            key = str(row.exe) + '_' + str(int(row.pid))
            if key not in procstat_exe:
                procstat_exe[key] = {}
                procstat_exe[key]['cpu_usage'] = []
                procstat_exe[key]['memory_rss'] = []
            procstat_exe[key]['cpu_usage'].append([temp_time, row.cpu_usage])
            procstat_exe[key]['memory_rss'].append([temp_time, row.memory_rss])
        procstat_ret[server] = procstat_exe

    return render(request, 'monitor/show_procstat.html', {"procstat_ret": json.dumps(procstat_ret)})


def show_servers(request):
    servers = ['zhugaoping', ]
    server_res = {}
    cpu_res = {}
    mem_res = {}
    for server in servers:
        cpu_info = models.CpuInfo.objects.filter(host=server)
        cpu_ret = {}
        usage_system = []
        usage_user = []
        usage_softirq = []
        usage_iowait = []
        for row in cpu_info:
            temp_time = int(time.mktime(row.time.timetuple())) * 1000
            usage_system.append([temp_time, row.usage_system])
            usage_user.append([temp_time, row.usage_user])
            usage_softirq.append([temp_time, row.usage_softirq])
            usage_iowait.append([temp_time, row.usage_iowait])
        cpu_ret['usage_system'] = usage_system
        cpu_ret['usage_user'] = usage_user
        cpu_ret['usage_softirq'] = usage_softirq
        cpu_ret['usage_iowait'] = usage_iowait
        cpu_res[server] = cpu_ret

        mem_info = models.MemoryInfo.objects.filter(host=server)
        mem_ret = []
        for row in mem_info:
            temp_time = int(time.mktime(row.time.timetuple()))*1000
            mem_ret.append([temp_time, row.used_percent])
        mem_res[server] = mem_ret

    server_res['cpu_res'] = cpu_res
    server_res['mem_res'] = mem_res

    return render(request, 'monitor/show_servers.html', {"server_res": json.dumps(server_res)})
