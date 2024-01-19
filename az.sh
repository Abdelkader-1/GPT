az ad sp create-for-rbac --name "abianalysis" --sdk-auth --role contributor --scopes /subscriptions/b47aa3c4-25c7-4b90-a5cd-87a81216f25f/resourceGroups/ABItest/providers/Microsoft.Web/sites/ABItest


az ad sp create-for-rbac --name "abianalysis" --role contributor \
                            --scopes /subscriptions/b47aa3c4-25c7-4b90-a5cd-87a81216f25f/resourceGroups/ABItest \
                            --sdk-auth


                            az ad sp create-for-rbac --name "abiassis" --role contributor \
                            --scopes /subscriptions/b47aa3c4-25c7-4b90-a5cd-87a81216f25f/resourceGroups/"abi2" \
                            --sdk-auth