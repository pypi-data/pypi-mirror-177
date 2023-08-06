基于[凌鲨](https://www.linksaas.pro)客户端本地api的python client

### demo

```python
from  linksaas_local_api import ApiClient,Configuration
from linksaas_local_api.apis import GlobalApi

cfg = Configuration(host="http://127.0.0.1:8001")
apiClient = ApiClient(configuration=cfg)
api = GlobalApi(api_client=apiClient)
res = api.hello_get()
print(res)
res = api.show_get()
print(res)
```

# 接口说明

## GlobalApi

| 接口      | 功能                     |
| --------- | ------------------------ |
| hello_get | 检查是否是linksaas客户端 |
| show_get  | 显示桌面端程序           |

## ProjectBugApi

| 接口                                                | 功能               |
| --------------------------------------------------- | ------------------ |
| project_project_id_bug_all_get                      | 列出所有缺陷       |
| project_project_id_bug_my_get                       | 列出指派给我的缺陷 |
| project_project_id_bug_record_bug_id_events_get     | 列出缺陷相关事件   |
| project_project_id_bug_record_bug_id_short_note_get | 便签方式显示缺陷   |
| project_project_id_bug_record_bug_id_show_get       | 在客户端显示缺陷   |

## ProjectCreateApi

| 接口                                           | 功能             |
| ---------------------------------------------- | ---------------- |
| project_project_id_create_bug_get              | 在客户端创建缺陷 |
| project_project_id_create_doc_doc_space_id_get | 在客户端创建文档 |
| project_project_id_create_task_get             | 在客户端创建任务 |

## ProjectDocApi

| 接口                                                      | 功能             |
| --------------------------------------------------------- | ---------------- |
| project_project_id_doc_space_doc_space_id_doc_id_show_get | 在客户端显示文档 |
| project_project_id_doc_space_doc_space_id_get             | 列出文档         |
| project_project_id_doc_space_get                          | 列出文档空间     |


## ProjectEventApi

| 接口                         | 功能         |
| ---------------------------- | ------------ |
| project_project_id_event_get | 列出事件列表 |

## ProjectMemberApi

| 接口                                              | 功能                 |
| ------------------------------------------------- | -------------------- |
| project_project_id_member_get                     | 列出项目成员列表     |
| project_project_id_member_member_user_id_show_get | 在客户端显示成员信息 |

## ProjectTaskApi

| 接口                                                  | 功能               |
| ----------------------------------------------------- | ------------------ |
| project_project_id_task_all_get                       | 列出所有任务       |
| project_project_id_task_my_get                        | 列出指派给我的任务 |
| project_project_id_task_record_task_id_events_get     | 列出任务相关事件   |
| project_project_id_task_record_task_id_short_note_get | 便签方式显示任务   |
| project_project_id_task_record_task_id_show_get       | 在客户端显示任务   |