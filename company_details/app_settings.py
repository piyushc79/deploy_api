COMPANY_KEYS = ['name', 'founded_at', 'description', 'funding_amount',
                'funding_date', 'investor', 'funding_stage', 'website',
                'social_info']

DATE_FORMATS = [
    '%d-%m-%y',
    '%d-%m-%Y',
    '%d/%m/%y',
    '%d/%m/%Y',
    '%d.%m.%y',
    '%d.%m.%Y',
    '%Y-%m-%d',
    '%d/%m/%y %H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
]
STAGES = ["Series A", "Series B", "Series C", "Series D", "Series E", "Series F"]
WEBSITE_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
