### A. Chức năng
- Copy file config restart pod consumer kafka

### B. Cài đặt 
- python3.8 -m mobio_restart_pod <group_name>

### Change log 
#### Version: 0.1.2 : Copy file config restart pod consumer kafka
- python3 -m mobio_restart_pod 
#### Version: 0.2.1 : Support liveness call lib
Thêm đoạn sau vào YAML consumer
- cd <root_folder_project>; python3.8 -m mobio_restart_pod <group_name>