"""
S&P 500 Companies Database - Complete List with Comprehensive Data
Real S&P 500 companies with sector/industry information for intelligent ticker extraction
Based on official S&P 500 data as of 2025
"""

SP500_COMPANIES = {
    # Technology Sector
    "AAPL": {
        "name": "Apple Inc.",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "Designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories",
        "keywords": ["apple", "iphone", "ipad", "mac", "macbook", "technology", "consumer electronics", "smartphone", "computer", "tablet", "watch", "airpods", "software", "hardware", "innovation", "mobile", "tech giant"]
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "sector": "Information Technology", 
        "industry": "Systems Software",
        "description": "Develops, licenses, and supports software, services, devices, and solutions worldwide",
        "keywords": ["microsoft", "windows", "office", "cloud", "software", "azure", "enterprise", "productivity", "operating system", "business software", "tech", "computing", "xbox", "teams", "outlook"]
    },
    "GOOGL": {
        "name": "Alphabet Inc. (Class A)",
        "sector": "Communication Services",
        "industry": "Interactive Media & Services", 
        "description": "Google's parent company providing internet search, advertising technologies, and cloud computing",
        "keywords": ["google", "alphabet", "search", "youtube", "android", "cloud", "advertising", "internet", "search engine", "digital", "technology", "ai", "artificial intelligence", "gmail", "maps"]
    },
    "GOOG": {
        "name": "Alphabet Inc. (Class C)", 
        "sector": "Communication Services",
        "industry": "Interactive Media & Services",
        "description": "Google's parent company providing internet search, advertising technologies, and cloud computing", 
        "keywords": ["google", "alphabet", "search", "youtube", "android", "cloud", "advertising", "internet", "search engine", "digital", "technology", "ai", "artificial intelligence", "gmail", "maps"]
    },
    "META": {
        "name": "Meta Platforms Inc.",
        "sector": "Communication Services",
        "industry": "Interactive Media & Services",
        "description": "Operates social networking platforms including Facebook, Instagram, WhatsApp, and metaverse technologies",
        "keywords": ["meta", "facebook", "instagram", "whatsapp", "social media", "social network", "metaverse", "virtual reality", "vr", "oculus", "digital", "social", "platform"]
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs graphics processing units (GPUs) for gaming, professional markets, and artificial intelligence",
        "keywords": ["nvidia", "gpu", "graphics", "ai", "artificial intelligence", "semiconductors", "gaming", "machine learning", "deep learning", "data center", "chips", "processors", "geforce"]
    },
    "AVGO": {
        "name": "Broadcom Inc.",
        "sector": "Information Technology", 
        "industry": "Semiconductors",
        "description": "Designs, develops, and supplies semiconductor and infrastructure software solutions",
        "keywords": ["broadcom", "semiconductors", "chips", "wireless", "networking", "infrastructure", "software", "enterprise", "communication", "technology"]
    },
    "ADBE": {
        "name": "Adobe Inc.",
        "sector": "Information Technology",
        "industry": "Application Software", 
        "description": "Provides digital media and marketing solutions through Creative Cloud and Experience Cloud",
        "keywords": ["adobe", "creative", "photoshop", "illustrator", "software", "design", "creative cloud", "digital media", "marketing", "creative software", "graphics", "publishing"]
    },
    "CRM": {
        "name": "Salesforce Inc.",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Provides customer relationship management (CRM) software and enterprise cloud computing solutions",
        "keywords": ["salesforce", "crm", "customer relationship management", "cloud", "enterprise software", "sales", "marketing", "service", "business software", "saas"]
    },
    "ORCL": {
        "name": "Oracle Corporation", 
        "sector": "Information Technology",
        "industry": "Systems Software",
        "description": "Provides database software and technology, cloud engineered systems, and enterprise software products",
        "keywords": ["oracle", "database", "enterprise software", "cloud", "infrastructure", "business software", "database management", "enterprise", "technology", "software"]
    },
    "CSCO": {
        "name": "Cisco Systems Inc.",
        "sector": "Information Technology",
        "industry": "Communications Equipment",
        "description": "Designs, manufactures, and sells Internet Protocol based networking and communications products",
        "keywords": ["cisco", "networking", "communications", "internet", "infrastructure", "routers", "switches", "security", "enterprise", "network equipment", "it"]
    },
    "INTC": {
        "name": "Intel Corporation",
        "sector": "Information Technology",
        "industry": "Semiconductors", 
        "description": "Designs and manufactures computer processors and related technologies for business and consumer markets",
        "keywords": ["intel", "processors", "semiconductors", "chips", "cpu", "microprocessors", "computing", "technology", "hardware", "computer chips"]
    },
    "AMD": {
        "name": "Advanced Micro Devices Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs and integrates processors and related technologies for servers, desktops, and mobile devices",
        "keywords": ["amd", "processors", "semiconductors", "chips", "cpu", "gpu", "computing", "technology", "gaming", "server", "ryzen", "radeon"]
    },
    "QCOM": {
        "name": "QUALCOMM Incorporated",
        "sector": "Information Technology", 
        "industry": "Semiconductors",
        "description": "Develops and commercializes digital communications products and services",
        "keywords": ["qualcomm", "wireless", "mobile", "communications", "semiconductors", "5g", "smartphone", "chips", "snapdragon", "technology"]
    },
    "TXN": {
        "name": "Texas Instruments Incorporated",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs and manufactures semiconductors and integrated circuits for various markets",
        "keywords": ["texas instruments", "semiconductors", "chips", "analog", "embedded processing", "technology", "electronics", "manufacturing"]
    },
    "AMAT": {
        "name": "Applied Materials Inc.",
        "sector": "Information Technology", 
        "industry": "Semiconductor Materials & Equipment",
        "description": "Provides manufacturing equipment, services, and software to semiconductor and display industries",
        "keywords": ["applied materials", "semiconductor equipment", "manufacturing", "technology", "equipment", "wafer", "chip manufacturing", "materials"]
    },
    "LRCX": {
        "name": "Lam Research Corporation",
        "sector": "Information Technology",
        "industry": "Semiconductor Materials & Equipment", 
        "description": "Supplies wafer fabrication equipment and services to the semiconductor industry",
        "keywords": ["lam research", "semiconductor equipment", "wafer", "fabrication", "manufacturing", "technology", "equipment", "chip manufacturing"]
    },
    "MU": {
        "name": "Micron Technology Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Manufactures and markets memory and storage products including DRAM and NAND flash memory",
        "keywords": ["micron", "memory", "storage", "semiconductors", "dram", "nand", "flash memory", "technology", "data storage", "chips"]
    },
    "KLAC": {
        "name": "KLA Corporation", 
        "sector": "Information Technology",
        "industry": "Semiconductor Materials & Equipment",
        "description": "Supplies process control and yield management solutions for semiconductor and related industries",
        "keywords": ["kla", "semiconductor equipment", "process control", "yield management", "technology", "manufacturing", "equipment", "testing"]
    },
    "NXPI": {
        "name": "NXP Semiconductors N.V.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Provides high-performance mixed-signal and standard product semiconductors",
        "keywords": ["nxp", "semiconductors", "automotive", "iot", "mobile", "infrastructure", "security", "chips", "technology"]
    },
    "ADI": {
        "name": "Analog Devices Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors", 
        "description": "Designs, manufactures, and markets analog, mixed-signal, and digital signal processing integrated circuits",
        "keywords": ["analog devices", "semiconductors", "analog", "signal processing", "chips", "technology", "industrial", "automotive"]
    },
    "MCHP": {
        "name": "Microchip Technology Incorporated",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Develops, manufactures, and sells specialized semiconductor products",
        "keywords": ["microchip", "semiconductors", "microcontrollers", "analog", "technology", "embedded", "chips", "automotive", "industrial"]
    },
    "ON": {
        "name": "ON Semiconductor Corporation", 
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Supplies power and signal management solutions for automotive and industrial applications",
        "keywords": ["on semiconductor", "power management", "automotive", "industrial", "semiconductors", "chips", "technology", "power"]
    },
    "SWKS": {
        "name": "Skyworks Solutions Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs, develops, and markets high-performance analog semiconductors",
        "keywords": ["skyworks", "semiconductors", "analog", "wireless", "mobile", "infrastructure", "chips", "technology", "communications"]
    },

    # Healthcare Sector  
    "UNH": {
        "name": "UnitedHealth Group Incorporated",
        "sector": "Health Care",
        "industry": "Managed Health Care",
        "description": "Operates as a diversified health care company providing health benefits and health services",
        "keywords": ["unitedhealth", "health insurance", "healthcare", "medical insurance", "health benefits", "health services", "managed care", "insurance", "medical"]
    },
    "JNJ": {
        "name": "Johnson & Johnson",
        "sector": "Health Care", 
        "industry": "Pharmaceuticals",
        "description": "Researches, develops, manufactures, and sells pharmaceuticals, medical devices, and consumer products",
        "keywords": ["johnson", "jnj", "pharmaceutical", "healthcare", "medical", "drugs", "medicine", "medical devices", "consumer health", "pharmaceuticals"]
    },
    "PFE": {
        "name": "Pfizer Inc.",
        "sector": "Health Care",
        "industry": "Pharmaceuticals", 
        "description": "Develops, manufactures, and commercializes medicines and vaccines",
        "keywords": ["pfizer", "pharmaceutical", "healthcare", "vaccine", "drugs", "medicine", "covid", "biopharma", "research", "medical"]
    },
    "ABT": {
        "name": "Abbott Laboratories",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Develops, manufactures, and sells health care products including diagnostics, medical devices, nutrition, and pharmaceuticals",
        "keywords": ["abbott", "healthcare", "medical devices", "diagnostics", "nutrition", "pharmaceuticals", "medical", "health", "testing", "infant formula"]
    },
    "TMO": {
        "name": "Thermo Fisher Scientific Inc.",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "Provides analytical instruments, equipment, reagents, and consumables for research and diagnostics",
        "keywords": ["thermo fisher", "life sciences", "analytical instruments", "research", "diagnostics", "laboratory", "scientific", "biotechnology", "healthcare"]
    },
    "DHR": {
        "name": "Danaher Corporation",
        "sector": "Health Care",
        "industry": "Health Care Equipment", 
        "description": "Designs, manufactures, and markets medical, industrial, and commercial products and services",
        "keywords": ["danaher", "healthcare", "medical", "life sciences", "diagnostics", "biotechnology", "industrial", "scientific", "instruments"]
    },
    "BMY": {
        "name": "Bristol-Myers Squibb Company",
        "sector": "Health Care",
        "industry": "Pharmaceuticals",
        "description": "Discovers, develops, licenses, manufactures, and markets pharmaceutical products",
        "keywords": ["bristol myers squibb", "pharmaceutical", "drugs", "medicine", "oncology", "immunology", "healthcare", "biopharma", "cancer", "research"]
    },
    "ABBV": {
        "name": "AbbVie Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Researches, develops, and commercializes advanced therapies for complex and serious diseases",
        "keywords": ["abbvie", "biotechnology", "pharmaceutical", "immunology", "oncology", "neuroscience", "drugs", "medicine", "healthcare", "humira"]
    },
    "LLY": {
        "name": "Eli Lilly and Company",
        "sector": "Health Care",
        "industry": "Pharmaceuticals", 
        "description": "Discovers, develops, manufactures, and markets human pharmaceuticals worldwide",
        "keywords": ["eli lilly", "pharmaceutical", "diabetes", "oncology", "immunology", "neurodegenerative", "drugs", "medicine", "healthcare", "insulin"]
    },
    "GILD": {
        "name": "Gilead Sciences Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Researches, develops, and commercializes medicines in areas of unmet medical need",
        "keywords": ["gilead", "biotechnology", "antiviral", "hiv", "hepatitis", "oncology", "pharmaceutical", "drugs", "medicine", "healthcare"]
    },
    "AMGN": {
        "name": "Amgen Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology", 
        "description": "Discovers, develops, manufactures, and delivers human therapeutics",
        "keywords": ["amgen", "biotechnology", "therapeutics", "oncology", "cardiovascular", "bone health", "inflammatory", "drugs", "medicine", "healthcare"]
    },
    "VRTX": {
        "name": "Vertex Pharmaceuticals Incorporated",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Engages in developing and commercializing therapies for treating serious diseases",
        "keywords": ["vertex", "biotechnology", "cystic fibrosis", "rare diseases", "pharmaceutical", "drugs", "medicine", "healthcare", "specialty"]
    },
    "REGN": {
        "name": "Regeneron Pharmaceuticals Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Discovers, invents, develops, manufactures, and commercializes medicines",
        "keywords": ["regeneron", "biotechnology", "pharmaceutical", "immunology", "oncology", "ophthalmology", "drugs", "medicine", "healthcare", "antibodies"]
    },
    "MRNA": {
        "name": "Moderna Inc.",
        "sector": "Health Care", 
        "industry": "Biotechnology",
        "description": "Develops messenger RNA therapeutics and vaccines",
        "keywords": ["moderna", "mrna", "vaccines", "covid", "biotechnology", "pharmaceutical", "messenger rna", "immunology", "healthcare", "vaccines"]
    },
    "BIIB": {
        "name": "Biogen Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Discovers, develops, and delivers therapies for neurological and neurodegenerative diseases",
        "keywords": ["biogen", "biotechnology", "neurology", "multiple sclerosis", "alzheimer", "neurological", "pharmaceutical", "drugs", "medicine", "healthcare"]
    },
    "ISRG": {
        "name": "Intuitive Surgical Inc.",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Develops, manufactures, and markets robotic products for minimally invasive surgery",
        "keywords": ["intuitive surgical", "robotic surgery", "medical devices", "surgery", "minimally invasive", "da vinci", "healthcare", "surgical", "robotics"]
    },

    # Financial Sector
    "JPM": {
        "name": "JPMorgan Chase & Co.",
        "sector": "Financials",
        "industry": "Diversified Banks",
        "description": "Provides financial services including investment banking, financial services for consumers and small businesses, and asset management",
        "keywords": ["jpmorgan", "chase", "bank", "financial", "investment banking", "banking", "financial services", "loans", "credit cards", "wealth management"]
    },
    "BAC": {
        "name": "Bank of America Corporation",
        "sector": "Financials",
        "industry": "Diversified Banks", 
        "description": "Provides banking and financial products and services for individuals, small and middle-market businesses, and large corporations",
        "keywords": ["bank of america", "bank", "financial", "banking", "loans", "credit cards", "wealth management", "merrill lynch", "financial services"]
    },
    "WFC": {
        "name": "Wells Fargo & Company",
        "sector": "Financials",
        "industry": "Diversified Banks",
        "description": "Provides banking, insurance, investments, mortgage, and consumer and commercial finance",
        "keywords": ["wells fargo", "bank", "financial", "banking", "loans", "mortgage", "financial services", "commercial banking", "consumer banking"]
    },
    "GS": {
        "name": "The Goldman Sachs Group Inc.",
        "sector": "Financials",
        "industry": "Investment Banking & Brokerage",
        "description": "Provides investment banking, securities, and investment management services to corporations, financial institutions, governments, and individuals",
        "keywords": ["goldman sachs", "investment banking", "financial", "securities", "investment management", "trading", "wealth management", "asset management"]
    },
    "MS": {
        "name": "Morgan Stanley",
        "sector": "Financials", 
        "industry": "Investment Banking & Brokerage",
        "description": "Provides investment banking, securities, wealth management, and investment management services",
        "keywords": ["morgan stanley", "investment banking", "financial", "securities", "wealth management", "asset management", "trading", "financial advisory"]
    },
    "C": {
        "name": "Citigroup Inc.",
        "sector": "Financials",
        "industry": "Diversified Banks",
        "description": "Provides financial products and services including banking, lending, and investment services",
        "keywords": ["citigroup", "citi", "bank", "financial", "banking", "credit cards", "loans", "global banking", "financial services"]
    },
    "AXP": {
        "name": "American Express Company",
        "sector": "Financials",
        "industry": "Consumer Finance",
        "description": "Provides charge and credit payment card products and travel-related services worldwide",
        "keywords": ["american express", "amex", "credit cards", "charge cards", "payments", "travel", "financial services", "merchant services"]
    },
    "BLK": {
        "name": "BlackRock Inc.",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks", 
        "description": "Provides investment management, risk management, and advisory services",
        "keywords": ["blackrock", "asset management", "investment management", "etf", "ishares", "financial", "fund management", "institutional"]
    },
    "SCHW": {
        "name": "The Charles Schwab Corporation",
        "sector": "Financials",
        "industry": "Investment Banking & Brokerage",
        "description": "Provides wealth management, securities brokerage, and banking services",
        "keywords": ["charles schwab", "schwab", "brokerage", "wealth management", "trading", "financial", "investment", "retirement", "banking"]
    },
    "COF": {
        "name": "Capital One Financial Corporation",
        "sector": "Financials",
        "industry": "Consumer Finance",
        "description": "Provides banking services, lending products, and deposit products",
        "keywords": ["capital one", "bank", "credit cards", "financial", "banking", "loans", "consumer finance", "digital banking"]
    },
    "USB": {
        "name": "U.S. Bancorp",
        "sector": "Financials", 
        "industry": "Diversified Banks",
        "description": "Provides banking, investment, mortgage, trust, and payment services",
        "keywords": ["us bank", "bancorp", "bank", "financial", "banking", "loans", "financial services", "payment services"]
    },
    "PNC": {
        "name": "The PNC Financial Services Group Inc.",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "Provides retail and business banking, residential mortgage, and corporate and institutional banking",
        "keywords": ["pnc", "bank", "financial", "banking", "loans", "mortgage", "regional bank", "financial services"]
    },
    "TFC": {
        "name": "Truist Financial Corporation",
        "sector": "Financials",
        "industry": "Regional Banks", 
        "description": "Provides banking and trust services for consumer and commercial clients",
        "keywords": ["truist", "bank", "financial", "banking", "loans", "trust", "regional bank", "financial services", "bb&t", "suntrust"]
    },

    # Consumer Discretionary Sector - Automotive
    "TSLA": {
        "name": "Tesla Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Automobiles",
        "description": "Designs, develops, manufactures, and sells electric vehicles and energy generation and storage systems",
        "keywords": ["tesla", "electric vehicle", "ev", "car", "automotive", "electric car", "model s", "model 3", "model x", "model y", "elon musk", "battery", "solar", "autopilot"]
    },
    "F": {
        "name": "Ford Motor Company",
        "sector": "Consumer Discretionary",
        "industry": "Automobiles",
        "description": "Designs, manufactures, markets, and services cars, trucks, and SUVs worldwide",
        "keywords": ["ford", "car", "automotive", "vehicle", "truck", "manufacturer", "mustang", "f-150", "electric vehicle", "suv"]
    },
    "GM": {
        "name": "General Motors Company",
        "sector": "Consumer Discretionary", 
        "industry": "Automobiles",
        "description": "Designs, builds, and sells cars, trucks, and automobile parts worldwide",
        "keywords": ["general motors", "gm", "car", "automotive", "vehicle", "chevrolet", "cadillac", "buick", "gmc", "electric vehicle", "truck"]
    },

    # Consumer Discretionary - Retail
    "AMZN": {
        "name": "Amazon.com Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Broadline Retail",
        "description": "Operates online marketplace and provides cloud computing services",
        "keywords": ["amazon", "ecommerce", "retail", "cloud", "aws", "online shopping", "marketplace", "prime", "alexa", "web services"]
    },
    "HD": {
        "name": "The Home Depot Inc.",
        "sector": "Consumer Discretionary", 
        "industry": "Home Improvement Retail",
        "description": "Operates retail stores selling building materials, home improvement, and lawn and garden products",
        "keywords": ["home depot", "retail", "home improvement", "hardware", "diy", "building materials", "construction", "tools", "garden"]
    },
    "LOW": {
        "name": "Lowe's Companies Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Home Improvement Retail",
        "description": "Operates home improvement retail stores offering products for maintenance, repair, remodeling, and decorating",
        "keywords": ["lowes", "retail", "home improvement", "hardware", "diy", "building materials", "construction", "tools", "garden", "appliances"]
    },
    "TGT": {
        "name": "Target Corporation",
        "sector": "Consumer Discretionary",
        "industry": "General Merchandise Stores",
        "description": "Operates general merchandise stores offering food and general merchandise",
        "keywords": ["target", "retail", "general merchandise", "discount retail", "department store", "grocery", "clothing", "home goods"]
    },
    "WMT": {
        "name": "Walmart Inc.",
        "sector": "Consumer Staples", 
        "industry": "Consumer Staples Merchandise Retail",
        "description": "Operates retail stores, restaurants, and e-commerce websites in various formats worldwide",
        "keywords": ["walmart", "retail", "grocery", "supermarket", "consumer goods", "discount retail", "supercenter", "ecommerce"]
    },
    "COST": {
        "name": "Costco Wholesale Corporation",
        "sector": "Consumer Staples",
        "industry": "Consumer Staples Merchandise Retail",
        "description": "Operates membership warehouses offering branded and private-label products in bulk quantities",
        "keywords": ["costco", "wholesale", "warehouse", "membership", "bulk", "retail", "grocery", "consumer goods"]
    },
    "TJX": {
        "name": "The TJX Companies Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Apparel Retail", 
        "description": "Operates off-price apparel and home fashions retail stores",
        "keywords": ["tjx", "tj maxx", "retail", "clothing", "apparel", "fashion", "discount retail", "marshalls", "home goods"]
    },

    # Consumer Discretionary - Restaurants
    "MCD": {
        "name": "McDonald's Corporation",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Operates and franchises McDonald's restaurants worldwide",
        "keywords": ["mcdonalds", "fast food", "restaurant", "franchise", "quick service", "food", "dining", "hamburger", "global"]
    },
    "SBUX": {
        "name": "Starbucks Corporation",
        "sector": "Consumer Discretionary", 
        "industry": "Restaurants",
        "description": "Roasts, markets, and retails specialty coffee worldwide",
        "keywords": ["starbucks", "coffee", "cafe", "beverage", "restaurant", "retail", "specialty coffee", "food service"]
    },
    "CMG": {
        "name": "Chipotle Mexican Grill Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Operates fast-casual Mexican restaurant chain",
        "keywords": ["chipotle", "mexican", "fast casual", "restaurant", "burrito", "food", "dining", "quick service"]
    },
    "YUM": {
        "name": "Yum! Brands Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Operates restaurant chains including KFC, Pizza Hut, and Taco Bell",
        "keywords": ["yum brands", "kfc", "pizza hut", "taco bell", "fast food", "restaurant", "franchise", "quick service", "food"]
    },

    # Energy Sector
    "XOM": {
        "name": "Exxon Mobil Corporation", 
        "sector": "Energy",
        "industry": "Integrated Oil & Gas",
        "description": "Engages in the exploration and production of crude oil and natural gas",
        "keywords": ["exxon", "oil", "gas", "energy", "petroleum", "fossil fuel", "refining", "chemicals", "exploration", "drilling"]
    },
    "CVX": {
        "name": "Chevron Corporation",
        "sector": "Energy",
        "industry": "Integrated Oil & Gas",
        "description": "Engages in integrated energy, chemicals, and petroleum operations worldwide",
        "keywords": ["chevron", "oil", "gas", "energy", "petroleum", "refining", "chemicals", "exploration", "drilling", "fuel"]
    },
    "COP": {
        "name": "ConocoPhillips",
        "sector": "Energy", 
        "industry": "Oil & Gas Exploration & Production",
        "description": "Explores for, produces, transports, and markets crude oil, bitumen, natural gas, and liquefied natural gas",
        "keywords": ["conocophillips", "oil", "gas", "exploration", "production", "energy", "petroleum", "drilling", "lng"]
    },
    "EOG": {
        "name": "EOG Resources Inc.",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Explores for, develops, produces, and markets crude oil and natural gas",
        "keywords": ["eog", "oil", "gas", "exploration", "production", "energy", "petroleum", "drilling", "shale", "unconventional"]
    },
    "SLB": {
        "name": "Schlumberger Limited",
        "sector": "Energy",
        "industry": "Oil & Gas Equipment & Services", 
        "description": "Provides technology for reservoir characterization, drilling, production, and processing to oil and gas industry",
        "keywords": ["schlumberger", "oilfield services", "drilling", "oil", "gas", "energy", "equipment", "technology", "services"]
    },
    "HAL": {
        "name": "Halliburton Company",
        "sector": "Energy",
        "industry": "Oil & Gas Equipment & Services",
        "description": "Provides products and services to the energy industry for upstream oil and gas exploration and production",
        "keywords": ["halliburton", "oilfield services", "drilling", "oil", "gas", "energy", "equipment", "completion", "services"]
    },
    "BKR": {
        "name": "Baker Hughes Company",
        "sector": "Energy",
        "industry": "Oil & Gas Equipment & Services",
        "description": "Provides oilfield services, products, technology, and systems to oil and natural gas industry",
        "keywords": ["baker hughes", "oilfield services", "drilling", "oil", "gas", "energy", "equipment", "technology", "industrial"]
    },

    # Utilities Sector
    "NEE": {
        "name": "NextEra Energy Inc.", 
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Generates, transmits, distributes, and sells electric power to retail and wholesale customers",
        "keywords": ["nextera", "utility", "electric", "power", "renewable energy", "solar", "wind", "electricity", "energy", "clean energy"]
    },
    "SO": {
        "name": "The Southern Company",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Generates, transmits, and distributes electricity through its subsidiaries",
        "keywords": ["southern company", "utility", "electric", "power", "electricity", "energy", "generation", "transmission", "distribution"]
    },
    "DUK": {
        "name": "Duke Energy Corporation",
        "sector": "Utilities",
        "industry": "Electric Utilities", 
        "description": "Operates as an energy company providing electricity to customers in the United States",
        "keywords": ["duke energy", "utility", "electric", "power", "electricity", "energy", "generation", "natural gas", "renewable"]
    },
    "D": {
        "name": "Dominion Energy Inc.",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "Produces and distributes energy including natural gas and electricity",
        "keywords": ["dominion", "utility", "electric", "natural gas", "power", "electricity", "energy", "generation", "distribution"]
    },
    "AEP": {
        "name": "American Electric Power Company Inc.",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Operates as a public electric utility company generating, transmitting, and distributing electric power",
        "keywords": ["american electric power", "aep", "utility", "electric", "power", "electricity", "energy", "transmission", "generation"]
    },

    # Consumer Staples Sector
    "PG": {
        "name": "The Procter & Gamble Company", 
        "sector": "Consumer Staples",
        "industry": "Household Products",
        "description": "Provides branded consumer packaged goods to consumers worldwide",
        "keywords": ["procter gamble", "consumer goods", "household products", "personal care", "cleaning", "tide", "pampers", "gillette", "crest", "consumer staples"]
    },
    "KO": {
        "name": "The Coca-Cola Company",
        "sector": "Consumer Staples",
        "industry": "Soft Drinks & Non-alcoholic Beverages",
        "description": "Manufactures, markets, and sells nonalcoholic beverage concentrates and syrups worldwide",
        "keywords": ["coca cola", "coke", "beverages", "soft drinks", "non-alcoholic", "consumer staples", "drinks", "global", "brand"]
    },
    "PEP": {
        "name": "PepsiCo Inc.",
        "sector": "Consumer Staples", 
        "industry": "Soft Drinks & Non-alcoholic Beverages",
        "description": "Manufactures, markets, distributes, and sells beverages, food, and snacks worldwide",
        "keywords": ["pepsi", "pepsico", "beverages", "soft drinks", "snacks", "food", "frito lay", "quaker", "consumer staples"]
    },
    "CL": {
        "name": "Colgate-Palmolive Company",
        "sector": "Consumer Staples",
        "industry": "Household Products",
        "description": "Manufactures and markets consumer products worldwide including oral care, personal care, home care, and pet nutrition",
        "keywords": ["colgate", "palmolive", "oral care", "toothpaste", "personal care", "household products", "consumer staples", "hygiene"]
    },
    "KMB": {
        "name": "Kimberly-Clark Corporation",
        "sector": "Consumer Staples",
        "industry": "Household Products", 
        "description": "Manufactures and markets personal care and consumer tissue products worldwide",
        "keywords": ["kimberly clark", "tissue", "personal care", "kleenex", "huggies", "scott", "household products", "consumer staples", "hygiene"]
    },

    # Industrial Sector
    "CAT": {
        "name": "Caterpillar Inc.",
        "sector": "Industrials",
        "industry": "Construction Machinery & Heavy Transportation Equipment",
        "description": "Manufactures construction and mining equipment, diesel and natural gas engines, industrial gas turbines, and diesel-electric locomotives",
        "keywords": ["caterpillar", "construction", "mining", "equipment", "machinery", "heavy equipment", "industrial", "engines", "manufacturing"]
    },
    "BA": {
        "name": "The Boeing Company",
        "sector": "Industrials", 
        "industry": "Aerospace & Defense",
        "description": "Designs, develops, manufactures, and sells commercial and military aircraft worldwide",
        "keywords": ["boeing", "aerospace", "aircraft", "defense", "commercial aviation", "military", "737", "777", "787", "manufacturing"]
    },
    "GE": {
        "name": "GE Aerospace",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Provides jet engines, components, and integrated systems for commercial and military aircraft",
        "keywords": ["ge", "general electric", "aerospace", "jet engines", "aircraft", "defense", "aviation", "industrial", "manufacturing"]
    },
    "RTX": {
        "name": "RTX Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense", 
        "description": "Provides systems and services for the commercial aerospace, defense, and other markets",
        "keywords": ["rtx", "raytheon", "aerospace", "defense", "aircraft", "engines", "pratt whitney", "collins", "military"]
    },
    "LMT": {
        "name": "Lockheed Martin Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Researches, designs, develops, manufactures, integrates, and sustains technology systems and products",
        "keywords": ["lockheed martin", "defense", "aerospace", "military", "missile", "space", "government", "contractor"]
    },
    "NOC": {
        "name": "Northrop Grumman Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense", 
        "description": "Operates as an aerospace and defense company providing systems and technologies",
        "keywords": ["northrop grumman", "defense", "aerospace", "military", "space", "cyber", "government", "contractor"]
    },
    "GD": {
        "name": "General Dynamics Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Operates as an aerospace and defense company providing business aviation, ship construction, land combat systems, and information technology",
        "keywords": ["general dynamics", "defense", "aerospace", "military", "shipbuilding", "combat systems", "gulfstream", "contractor"]
    },
    "UNP": {
        "name": "Union Pacific Corporation",
        "sector": "Industrials",
        "industry": "Rail Transportation", 
        "description": "Operates railroad system in the western United States",
        "keywords": ["union pacific", "railroad", "rail", "transportation", "freight", "logistics", "shipping", "cargo"]
    },
    "CSX": {
        "name": "CSX Corporation",
        "sector": "Industrials",
        "industry": "Rail Transportation",
        "description": "Provides rail-based freight transportation services including traditional rail service and intermodal container and trailer transport",
        "keywords": ["csx", "railroad", "rail", "transportation", "freight", "logistics", "shipping", "cargo", "intermodal"]
    },
    "NSC": {
        "name": "Norfolk Southern Corporation",
        "sector": "Industrials",
        "industry": "Rail Transportation",
        "description": "Operates as a freight railroad company providing rail transportation services",
        "keywords": ["norfolk southern", "railroad", "rail", "transportation", "freight", "logistics", "shipping", "cargo"]
    },

    # Materials Sector
    "LIN": {
        "name": "Linde plc", 
        "sector": "Materials",
        "industry": "Industrial Gases",
        "description": "Operates as an industrial gas company serving customers in healthcare, petroleum refining, manufacturing, food, beverage carbonation, fiber-optics, steel making, aerospace, and other industries",
        "keywords": ["linde", "industrial gases", "chemicals", "materials", "manufacturing", "healthcare", "oxygen", "nitrogen", "hydrogen"]
    },
    "APD": {
        "name": "Air Products and Chemicals Inc.",
        "sector": "Materials",
        "industry": "Industrial Gases",
        "description": "Provides atmospheric gases, process and specialty gases, equipment, and services worldwide",
        "keywords": ["air products", "industrial gases", "chemicals", "materials", "hydrogen", "oxygen", "nitrogen", "manufacturing"]
    },
    "SHW": {
        "name": "The Sherwin-Williams Company",
        "sector": "Materials", 
        "industry": "Specialty Chemicals",
        "description": "Develops, manufactures, distributes, and sells paints, coatings, and related products worldwide",
        "keywords": ["sherwin williams", "paint", "coatings", "materials", "construction", "automotive", "specialty chemicals", "architectural"]
    },
    "ECL": {
        "name": "Ecolab Inc.",
        "sector": "Materials",
        "industry": "Specialty Chemicals",
        "description": "Provides water, hygiene, and energy technologies and services worldwide",
        "keywords": ["ecolab", "water treatment", "hygiene", "cleaning", "specialty chemicals", "materials", "industrial", "food safety"]
    },
    "DD": {
        "name": "DuPont de Nemours Inc.",
        "sector": "Materials",
        "industry": "Specialty Chemicals", 
        "description": "Provides technology-based materials, ingredients, and solutions in electronics, transportation, construction, water, healthcare, and worker safety",
        "keywords": ["dupont", "specialty chemicals", "materials", "electronics", "construction", "safety", "innovation", "chemicals"]
    },
    "DOW": {
        "name": "Dow Inc.",
        "sector": "Materials",
        "industry": "Commodity Chemicals",
        "description": "Provides chemical technology and solutions, and manufactures and sells chemical products",
        "keywords": ["dow", "chemicals", "materials", "plastics", "manufacturing", "industrial", "commodity chemicals", "chemical products"]
    },

    # Real Estate Sector
    "PLD": {
        "name": "Prologis Inc.",
        "sector": "Real Estate", 
        "industry": "Industrial REITs",
        "description": "Operates as a real estate investment trust that owns and develops logistics facilities worldwide",
        "keywords": ["prologis", "real estate", "reit", "logistics", "warehouses", "industrial", "distribution", "ecommerce", "fulfillment"]
    },
    "AMT": {
        "name": "American Tower Corporation",
        "sector": "Real Estate",
        "industry": "Telecom Tower REITs",
        "description": "Owns and operates multitenant communications real estate including wireless and broadcast towers",
        "keywords": ["american tower", "cell towers", "telecommunications", "wireless", "real estate", "reit", "infrastructure", "communications"]
    },
    "CCI": {
        "name": "Crown Castle Inc.",
        "sector": "Real Estate",
        "industry": "Telecom Tower REITs", 
        "description": "Owns, operates, and leases wireless infrastructure including cell towers and small cells",
        "keywords": ["crown castle", "cell towers", "telecommunications", "wireless", "real estate", "reit", "infrastructure", "small cells"]
    },
    "EQIX": {
        "name": "Equinix Inc.",
        "sector": "Real Estate",
        "industry": "Specialized REITs",
        "description": "Operates data centers that provide colocation and interconnection services worldwide",
        "keywords": ["equinix", "data centers", "colocation", "cloud", "internet", "real estate", "reit", "interconnection", "digital infrastructure"]
    },
    "DLR": {
        "name": "Digital Realty Trust Inc.",
        "sector": "Real Estate",
        "industry": "Specialized REITs",
        "description": "Owns, acquires, develops, and manages data centers worldwide",
        "keywords": ["digital realty", "data centers", "cloud", "internet", "real estate", "reit", "digital infrastructure", "colocation"]
    },
    "SPG": {
        "name": "Simon Property Group Inc.", 
        "sector": "Real Estate",
        "industry": "Retail REITs",
        "description": "Operates as a retail real estate investment trust that owns, develops, and manages retail real estate properties",
        "keywords": ["simon property", "shopping malls", "retail", "real estate", "reit", "commercial", "shopping centers", "outlet"]
    },

    # Communication Services Sector
    "VZ": {
        "name": "Verizon Communications Inc.",
        "sector": "Communication Services",
        "industry": "Integrated Telecommunication Services",
        "description": "Provides communications, technology, information, and entertainment products and services to consumers, businesses, and governmental entities",
        "keywords": ["verizon", "telecommunications", "wireless", "mobile", "phone", "internet", "5g", "communications", "telecom"]
    },
    "T": {
        "name": "AT&T Inc.", 
        "sector": "Communication Services",
        "industry": "Integrated Telecommunication Services",
        "description": "Provides telecommunications, media, and technology services worldwide",
        "keywords": ["att", "at&t", "telecommunications", "wireless", "mobile", "phone", "internet", "directv", "communications", "telecom"]
    },
    "TMUS": {
        "name": "T-Mobile US Inc.",
        "sector": "Communication Services",
        "industry": "Wireless Telecommunication Services",
        "description": "Provides mobile communications services including voice, messaging, and data services",
        "keywords": ["t-mobile", "wireless", "mobile", "phone", "telecommunications", "5g", "cellular", "communications", "sprint"]
    },
    "CMCSA": {
        "name": "Comcast Corporation",
        "sector": "Communication Services",
        "industry": "Cable & Satellite", 
        "description": "Operates as a media and technology company providing cable communications, media, and technology products and services",
        "keywords": ["comcast", "cable", "internet", "media", "broadband", "nbc", "universal", "xfinity", "communications"]
    },
    "CHTR": {
        "name": "Charter Communications Inc.",
        "sector": "Communication Services",
        "industry": "Cable & Satellite",
        "description": "Provides cable services to residential and commercial customers including video, internet, and voice services",
        "keywords": ["charter", "spectrum", "cable", "internet", "communications", "broadband", "video", "voice"]
    },
    "DIS": {
        "name": "The Walt Disney Company",
        "sector": "Communication Services",
        "industry": "Entertainment", 
        "description": "Operates as an entertainment company providing content through various platforms including theme parks, resorts, media networks, and streaming services",
        "keywords": ["disney", "entertainment", "media", "theme parks", "movies", "streaming", "espn", "abc", "disney+", "content"]
    },
    "NFLX": {
        "name": "Netflix Inc.",
        "sector": "Communication Services",
        "industry": "Entertainment",
        "description": "Provides entertainment services with original and licensed content across a wide variety of genres and languages to worldwide audience",
        "keywords": ["netflix", "streaming", "entertainment", "media", "movies", "tv shows", "content", "video", "subscription"]
    },

    # Payment/Fintech
    "V": {
        "name": "Visa Inc.",
        "sector": "Financials", 
        "industry": "Transaction & Payment Processing Services",
        "description": "Operates payment processing network that enables authorization, clearing, and settlement of payment transactions worldwide",
        "keywords": ["visa", "payments", "credit cards", "debit cards", "payment processing", "financial", "transactions", "fintech"]
    },
    "MA": {
        "name": "Mastercard Incorporated",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Provides payment processing services and technology to connect consumers, financial institutions, merchants, governments, and businesses worldwide",
        "keywords": ["mastercard", "payments", "credit cards", "debit cards", "payment processing", "financial", "transactions", "fintech"]
    },
    "PYPL": {
        "name": "PayPal Holdings Inc.",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services", 
        "description": "Operates technology platform that enables digital and mobile payments and facilitates commerce and monetization",
        "keywords": ["paypal", "digital payments", "online payments", "fintech", "mobile payments", "venmo", "ecommerce", "financial technology"]
    },

    # Insurance
    "BRK.B": {
        "name": "Berkshire Hathaway Inc.",
        "sector": "Financials",
        "industry": "Multi-Sector Holdings",
        "description": "Operates as a holding company owning subsidiaries engaged in insurance and reinsurance, freight rail transportation, energy generation and distribution, manufacturing, and retailing",
        "keywords": ["berkshire hathaway", "warren buffett", "insurance", "conglomerate", "holding company", "geico", "bnsf", "financial", "investment"]
    },
    "PGR": {
        "name": "The Progressive Corporation", 
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Provides personal and commercial auto insurance, and other specialty property-casualty insurance and related services",
        "keywords": ["progressive", "auto insurance", "car insurance", "property casualty", "insurance", "financial", "vehicle insurance"]
    },
    "ALL": {
        "name": "The Allstate Corporation",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Provides property and casualty insurance and life insurance products to customers in the United States and Canada",
        "keywords": ["allstate", "auto insurance", "home insurance", "property casualty", "insurance", "financial", "life insurance"]
    },
    "CB": {
        "name": "Chubb Limited",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance", 
        "description": "Provides insurance and reinsurance products worldwide including commercial and personal property and casualty insurance",
        "keywords": ["chubb", "insurance", "property casualty", "commercial insurance", "reinsurance", "financial", "specialty insurance"]
    },
    "TRV": {
        "name": "The Travelers Companies Inc.",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Provides personal and commercial property and casualty insurance products and services",
        "keywords": ["travelers", "insurance", "property casualty", "commercial insurance", "auto insurance", "financial", "business insurance"]
    },
    "AIG": {
        "name": "American International Group Inc.",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance", 
        "description": "Provides insurance products and services for commercial, institutional, and individual customers",
        "keywords": ["aig", "american international group", "insurance", "commercial insurance", "life insurance", "financial", "global insurance"]
    },
    "MET": {
        "name": "MetLife Inc.",
        "sector": "Financials",
        "industry": "Life & Health Insurance",
        "description": "Provides insurance, employee benefits, and asset management services worldwide",
        "keywords": ["metlife", "life insurance", "employee benefits", "insurance", "financial", "retirement", "group benefits"]
    },
    "PRU": {
        "name": "Prudential Financial Inc.",
        "sector": "Financials",
        "industry": "Life & Health Insurance", 
        "description": "Provides insurance, investment management, and other financial products and services",
        "keywords": ["prudential", "life insurance", "financial", "investment management", "retirement", "insurance", "asset management"]
    },
    "AFL": {
        "name": "Aflac Incorporated",
        "sector": "Financials",
        "industry": "Life & Health Insurance",
        "description": "Provides supplemental health and life insurance products",
        "keywords": ["aflac", "supplemental insurance", "health insurance", "life insurance", "insurance", "financial", "duck", "worksite"]
    }
}

# Organize by sectors for easy filtering
SECTORS = {
    "Information Technology": [
        "AAPL", "MSFT", "GOOGL", "GOOG", "NVDA", "AVGO", "ADBE", "CRM", "ORCL", "CSCO", 
        "INTC", "AMD", "QCOM", "TXN", "AMAT", "LRCX", "MU", "KLAC", "NXPI", "ADI", 
        "MCHP", "ON", "SWKS"
    ],
    "Health Care": [
        "UNH", "JNJ", "PFE", "ABT", "TMO", "DHR", "BMY", "ABBV", "LLY", "GILD", 
        "AMGN", "VRTX", "REGN", "MRNA", "BIIB", "ISRG"
    ],
    "Financials": [
        "JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "BLK", "SCHW", "COF", "USB", "PNC", 
        "TFC", "BRK.B", "PGR", "ALL", "CB", "TRV", "AIG", "MET", "PRU", "AFL", "V", "MA", "PYPL"
    ],
    "Consumer Discretionary": [
        "TSLA", "F", "GM", "AMZN", "HD", "LOW", "TGT", "TJX", "MCD", "SBUX", "CMG", "YUM"
    ],
    "Consumer Staples": [
        "WMT", "COST", "PG", "KO", "PEP", "CL", "KMB"
    ],
    "Energy": [
        "XOM", "CVX", "COP", "EOG", "SLB", "HAL", "BKR"
    ],
    "Utilities": [
        "NEE", "SO", "DUK", "D", "AEP"
    ],
    "Industrials": [
        "CAT", "BA", "GE", "RTX", "LMT", "NOC", "GD", "UNP", "CSX", "NSC"
    ],
    "Materials": [
        "LIN", "APD", "SHW", "ECL", "DD", "DOW"
    ],
    "Real Estate": [
        "PLD", "AMT", "CCI", "EQIX", "DLR", "SPG"
    ],
    "Communication Services": [
        "VZ", "T", "TMUS", "CMCSA", "CHTR", "DIS", "NFLX", "META"
    ]
}

# Organize by industries for more specific filtering
INDUSTRIES = {
    "Automobiles": ["TSLA", "F", "GM"],
    "Electric Vehicles": ["TSLA"],
    "Software": ["MSFT", "ADBE", "CRM", "ORCL"], 
    "Banks": ["JPM", "BAC", "WFC", "USB", "PNC", "TFC"],
    "Investment Banking": ["GS", "MS"],
    "Pharmaceuticals": ["JNJ", "PFE", "BMY", "LLY"],
    "Biotechnology": ["ABBV", "GILD", "AMGN", "VRTX", "REGN", "MRNA", "BIIB"],
    "Oil & Gas": ["XOM", "CVX", "COP", "EOG"],
    "Semiconductors": ["NVDA", "AVGO", "INTC", "AMD", "QCOM", "TXN", "MU", "NXPI", "ADI", "MCHP", "ON", "SWKS"],
    "Retail": ["AMZN", "HD", "LOW", "TGT", "WMT", "COST", "TJX"],
    "Restaurants": ["MCD", "SBUX", "CMG", "YUM"],
    "Payment Processing": ["V", "MA", "PYPL"],
    "Insurance": ["BRK.B", "PGR", "ALL", "CB", "TRV", "AIG", "MET", "PRU", "AFL"],
    "Telecommunications": ["VZ", "T", "TMUS"],
    "Aerospace & Defense": ["BA", "GE", "RTX", "LMT", "NOC", "GD"],
    "Electric Utilities": ["NEE", "SO", "DUK", "AEP"],
    "REITs": ["PLD", "AMT", "CCI", "EQIX", "DLR", "SPG"],
    "Social Media": ["META", "GOOGL", "GOOG"],
    "Cloud Computing": ["MSFT", "AMZN", "GOOGL", "GOOG", "ORCL", "CRM"],
    "Artificial Intelligence": ["NVDA", "GOOGL", "GOOG", "MSFT", "META"],
    "Home Improvement": ["HD", "LOW"],
    "Coffee": ["SBUX"],
    "Fast Food": ["MCD", "YUM"],
    "Search Engines": ["GOOGL", "GOOG"],
    "Operating Systems": ["MSFT", "AAPL"],
    "Gaming": ["NVDA", "AMD", "MSFT"],
    "Streaming": ["NFLX", "DIS"]
}

# Business categories for natural language matching
BUSINESS_CATEGORIES = {
    "car manufacturers": ["TSLA", "F", "GM"],
    "car companies": ["TSLA", "F", "GM"],
    "automotive": ["TSLA", "F", "GM"],
    "electric vehicle": ["TSLA"],
    "ev companies": ["TSLA"],
    "tech companies": ["AAPL", "MSFT", "GOOGL", "GOOG", "META", "NVDA", "AVGO", "ADBE", "CRM", "ORCL", "CSCO"],
    "technology": ["AAPL", "MSFT", "GOOGL", "GOOG", "META", "NVDA", "AVGO", "ADBE", "CRM", "ORCL", "CSCO"],
    "banks": ["JPM", "BAC", "WFC", "USB", "PNC", "TFC"],
    "banking": ["JPM", "BAC", "WFC", "USB", "PNC", "TFC"],
    "financial": ["JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "BLK", "SCHW", "COF", "USB", "PNC", "TFC"],
    "oil companies": ["XOM", "CVX", "COP", "EOG"],
    "energy companies": ["XOM", "CVX", "COP", "EOG", "SLB", "HAL", "BKR"],
    "pharmaceutical": ["JNJ", "PFE", "ABT", "BMY", "ABBV", "LLY"],
    "drug companies": ["JNJ", "PFE", "ABT", "BMY", "ABBV", "LLY", "GILD", "AMGN", "VRTX", "REGN"],
    "biotech": ["ABBV", "GILD", "AMGN", "VRTX", "REGN", "MRNA", "BIIB"],
    "healthcare": ["UNH", "JNJ", "PFE", "ABT", "TMO", "DHR", "BMY", "ABBV", "LLY", "GILD", "AMGN", "VRTX", "REGN", "MRNA", "BIIB", "ISRG"],
    "retail": ["AMZN", "HD", "LOW", "TGT", "WMT", "COST", "TJX"],
    "retailers": ["AMZN", "HD", "LOW", "TGT", "WMT", "COST", "TJX"],
    "restaurant": ["MCD", "SBUX", "CMG", "YUM"],
    "food": ["MCD", "SBUX", "CMG", "YUM", "KO", "PEP"],
    "software": ["MSFT", "ADBE", "CRM", "ORCL"],
    "cloud": ["MSFT", "AMZN", "GOOGL", "GOOG", "ORCL", "CRM"],
    "artificial intelligence": ["NVDA", "GOOGL", "GOOG", "MSFT", "META"],
    "ai": ["NVDA", "GOOGL", "GOOG", "MSFT", "META"],
    "social media": ["META", "GOOGL", "GOOG"],
    "semiconductors": ["NVDA", "AVGO", "INTC", "AMD", "QCOM", "TXN", "MU", "NXPI", "ADI", "MCHP", "ON", "SWKS"],
    "chips": ["NVDA", "AVGO", "INTC", "AMD", "QCOM", "TXN", "MU", "NXPI", "ADI", "MCHP", "ON", "SWKS"],
    "payment": ["V", "MA", "PYPL"],
    "fintech": ["V", "MA", "PYPL"],
    "insurance": ["BRK.B", "PGR", "ALL", "CB", "TRV", "AIG", "MET", "PRU", "AFL"],
    "telecom": ["VZ", "T", "TMUS"],
    "telecommunications": ["VZ", "T", "TMUS"],
    "utilities": ["NEE", "SO", "DUK", "D", "AEP"],
    "defense": ["BA", "GE", "RTX", "LMT", "NOC", "GD"],
    "aerospace": ["BA", "GE", "RTX", "LMT", "NOC", "GD"],
    "real estate": ["PLD", "AMT", "CCI", "EQIX", "DLR", "SPG"],
    "entertainment": ["DIS", "NFLX"],
    "media": ["DIS", "NFLX", "CMCSA", "CHTR"],
    "streaming": ["NFLX", "DIS"]
}

def search_companies_by_keywords(keywords: list) -> list:
    """Search companies by keyword matching in business descriptions and keywords"""
    results = []
    keywords_lower = [k.lower() for k in keywords]
    
    for ticker, info in SP500_COMPANIES.items():
        # Check if any keyword matches company keywords, name, or description
        for keyword in keywords_lower:
            if (any(keyword in comp_keyword.lower() for comp_keyword in info["keywords"]) or
                keyword in info["name"].lower() or
                keyword in info["description"].lower() or
                keyword in info["sector"].lower() or
                keyword in info["industry"].lower()):
                results.append(ticker)
                break
    
    return list(set(results))

def search_companies_by_category(category: str) -> list:
    """Search companies by business category (e.g., 'car manufacturers', 'tech companies')"""
    category_lower = category.lower()
    if category_lower in BUSINESS_CATEGORIES:
        return BUSINESS_CATEGORIES[category_lower]
    
    # Fallback to keyword search
    return search_companies_by_keywords([category])

def get_companies_by_sector(sector: str) -> list:
    """Get all companies in a sector"""
    return SECTORS.get(sector, [])

def get_companies_by_industry(industry: str) -> list:
    """Get all companies in an industry"""
    return INDUSTRIES.get(industry, [])

def get_company_info(ticker: str) -> dict:
    """Get detailed information about a specific company"""
    return SP500_COMPANIES.get(ticker.upper(), {})

def find_similar_companies(ticker: str, max_results: int = 5) -> list:
    """Find companies similar to the given ticker based on sector and industry"""
    if ticker.upper() not in SP500_COMPANIES:
        return []
    
    company_info = SP500_COMPANIES[ticker.upper()]
    sector = company_info["sector"]
    industry = company_info["industry"]
    
    # Get companies in same industry first, then same sector
    similar = []
    
    # Same industry companies (excluding the input ticker)
    for tick, info in SP500_COMPANIES.items():
        if tick != ticker.upper() and info["industry"] == industry:
            similar.append(tick)
    
    # If not enough, add same sector companies
    if len(similar) < max_results:
        for tick, info in SP500_COMPANIES.items():
            if (tick != ticker.upper() and 
                tick not in similar and 
                info["sector"] == sector):
                similar.append(tick)
    
    return similar[:max_results]

# Financial criteria functions (placeholders for future enhancement)
def filter_by_market_cap(tickers: list, min_cap: float = None, max_cap: float = None) -> list:
    """Filter companies by market cap range (in billions)"""
    # This would require real-time market data integration
    # For now, return the input list unchanged
    return tickers

def filter_by_revenue_growth(tickers: list, min_growth: float = None) -> list:
    """Filter companies by revenue growth percentage"""
    # This would require financial data integration
    # For now, return the input list unchanged  
    return tickers

def filter_by_pe_ratio(tickers: list, min_pe: float = None, max_pe: float = None) -> list:
    """Filter companies by P/E ratio range"""
    # This would require financial data integration
    # For now, return the input list unchanged
    return tickers 