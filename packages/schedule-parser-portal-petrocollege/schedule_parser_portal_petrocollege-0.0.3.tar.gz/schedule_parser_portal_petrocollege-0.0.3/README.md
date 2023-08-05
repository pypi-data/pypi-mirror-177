# Simple parser portal (SharePoint) petrocollege

## Installation 

```cmd
pip install schedule_parser_portal_petrocollege
```

## Use SharePoint сlass

Create object of class SharePoint

```python
import SharePoint

share_point = SharePoint(username, password)
```


### Send any Request to server

```python

# Return Response JSON result
result = share_point.get_request_json(<some_url>)
```

### Get json object elements of List

```python
# result make list of title and link elements 

links = share_point.get_data_from_lists_type(result)

print(links)

#[            {
#                "title": Title,
#                "link" : "Lists(guid'9c095153-274d-4c73-9b8b-4e3dd6af89e5')/Items(16)"
#            }
#]

```
### Get files (AttachmentFiles)

```python

# url_list is a link like "Lists(guid'9c095153-274d-4c73-9b8b-4e3dd6af89e5')/Items(16)"
files = share_point.get_data_from_attachment_files_type((share_point.get_request_json(<url_list> + "/AttachmentFiles")))

#save files 

for file in files:
    share_point.save_file_by_url(file['ServerRelativeUrl'], file['FileName'], 'files')

```

## Get dict from file

```python

import File
file = ExcelFile('<path_to_xlsx_file>')
data = file.get_object()

```

return dict like 

```
{
            'teacher': 'Ярошенко С.П.',
            'debug_column': 324,
            'teacher_lessons':
                [
                    {
                        'lesson':
                            {
                                'discipline': 'Теор.гос.и права',
                                'room': '101',
                                'building': '4',
                                'groups': ['11-29'],
                                 '_Lesson__current_string': 'Теор.гос.и права  4/101',
                                'is_dop': False,
                                'subgroup': 0
                            },
                            'date_lesson': datetime.datetime(2022, 9, 1, 0, 0),
                            'number_of_lesson': 2,
                            'debug_position_row': 21,
                            'debug_position_column': 324,
                            'debug_position_coordinate': 'LL21'
                            }
                    }
                    ...
                ]
        }
```

