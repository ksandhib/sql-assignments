import csv

# Read the CSV file
restaurants = []
with open('Jomato.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            rating = float(row['Rating']) if row['Rating'] else None
            if rating is not None:
                restaurants.append({
                    'name': row['RestaurantName'],
                    'rating': rating,
                    'type': row['RestaurantType'],
                    'cost': row['AverageCost'],
                    'cuisines': row['CuisinesType']
                })
        except ValueError:
            continue

# Sort by rating descending
restaurants.sort(key=lambda x: x['rating'], reverse=True)

# Print top 5
print("Top 5 Restaurants by Rating:")
for i, rest in enumerate(restaurants[:5], 1):
    print(f"{i}. {rest['name']} - Rating: {rest['rating']} - Type: {rest['type']} - Avg Cost: {rest['cost']} - Cuisines: {rest['cuisines']}")
