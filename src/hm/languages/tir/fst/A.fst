# A -> e when not word initial
# A -> a when word initial (except following initial ')

-> start

start -> start  [']
start -> mid    [X-';V-A;/;a:A]
mid -> mid      [X;V-A;_;/;$;e:A]

mid ->
