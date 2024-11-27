for file in *2024*.csv; do
    year="2024"  # Year is fixed
    month=$(echo "$file" | grep -oP '^\w+(?=2024)') # Extract the month name
    number=$(echo "$file" | grep -oP '(?<=_)\d+(?=\.csv)') # Extract the numeric part
    new_file="BOA_${year}_${month}_${number}.csv" # Construct the new file name

    # Debugging Output
    echo "Renaming $file to $new_file"

    # Rename File
    mv "$file" "$new_file"
done

