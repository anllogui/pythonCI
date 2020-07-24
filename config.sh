file="./build.properties"

if [ -f "$file" ]
then
    echo "$file found."
    while IFS='=' read -r key value
    do
        key=$(echo $key | tr '.' '_')
	eval ${key}=\${value}
    done < "$file"
    echo "Model Version = " ${model_version}
    echo "Data Version  = " ${data_version}
    else
        echo "$file not found."
fi

