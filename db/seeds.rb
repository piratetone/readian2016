# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

Link.create!(title: 'NYTimes', label: 'liberal')
Link.create!(title: 'WSJ', label: 'conservative')
Link.create!(title: 'LA Times', label: 'liberal')
Link.create!(title: 'NRO', label: 'conservative')
Link.create!(title: 'The Week', label: 'moderate')
