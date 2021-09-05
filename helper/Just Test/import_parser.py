test = {"path": "./assets/taskmgr/a", "children":[{"path": "./assets/taskmgr/a/b", "children":[{"path": "./assets/taskmgr/a/b/c", "children":[]}]},{"path": "./assets/taskmgr/a/b2", "children":[]}]}

use = [{"path": "./assets/taskmgr/a", "children":[]}, {"path": "./assets/taskmgr/a/b", "children":[]}, {"path": "./assets/taskmgr/a/b2", "children":[]}, {"path": "./assets/taskmgr/a/b/c", "children":[]}]

for u in use:
    print('\n')
    splited = u['path'].split('/')
    # print('\n조갠것 : {}\n'.format(splited))
    
    group = list()
    for s in range(len(splited) - 4):
        group.append('/'.join(splited[ 0 : (s + 4) ]))
    print(u)
    print(group)

glist = [use[0]]
