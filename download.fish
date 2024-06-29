for i in (cat files.txt )
    set name  (string split '/' $i)[-2]
    wget $i -O $name
end
