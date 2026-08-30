# Xianyu bundle contract negative tests

1. `external_actions.publish=true`必须失败。
2. `external_actions.send_message=true`必须失败。
3. `rights.status=PENDING`必须失败批准。
4. `rights.status=BLOCKED`必须失败批准。
5. X2包含非空delivery_catalog必须失败。
6. reply rule mode为`auto_send`必须失败。
7. 修改任一清单内文件，manifest验证必须失败。
8. 增加未列文件必须失败。
9. Bundle ID含路径分隔符必须失败。
10. `package.sha256.txt`与manifest不一致必须失败。
