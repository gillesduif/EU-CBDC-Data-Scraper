import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
from urllib.parse import urlparse
import urllib.request
import random
from googleapiclient.discovery import build

class CBDCScraper:
    def __init__(self, api_key, cse_id, output_dir="./cbdc_data"):
        """
        Initializes the CBDC Scraper.
        
        Args:
            api_key (str): Google Custom Search Engine API key
            cse_id (str): Google Custom Search Engine ID
            output_dir (str): Directory to store downloaded files
        """
        self.api_key = api_key
        self.cse_id = cse_id
        self.output_dir = output_dir
        self.search_queries = {
            "white_papers": [
                '"CBDC" OR "digital euro" filetype:pdf',
                '"digital euro white paper" site:.eu filetype:pdf',
                '"central bank digital currency" AND "legal framework" filetype:pdf'
            ],
            "official_websites": [
                'site:ecb.europa.eu "digital euro"',
                'site:europa.eu "CBDC legal framework"',
                'site:ceps.eu "digital euro report"'
            ],
            "legal_documents": [
                '"CBDC regulation" OR "digital euro law" filetype:pdf',
                '"MiCA regulation" AND "CBDC" site:.eu',
                '"CBDC compliance" AND "European Union"'
            ],
            "specific_topics": [
                '"privacy challenges" AND "CBDC"',
                '"AML compliance" AND "digital euro"',
                '"technical design" AND "central bank digital currency"'
            ],
            "academic_publications": [
                'site:ssrn.com "CBDC artificial intelligence"',
                'site:mpra.ub.uni-muenchen.de "digital euro"',
                '"CBDC research paper" site:.edu'
            ],
            "interoperability": [
                '"DLT interoperability" AND "CBDC"',
                '"blockchain infrastructure" AND "digital euro"'
            ]
        }
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Create subdirectories for each category
        for category in self.search_queries.keys():
            category_dir = os.path.join(output_dir, category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
        
        # Data storage
        self.results_df = pd.DataFrame(columns=[
            'title', 'link', 'snippet', 'source', 'category', 
            'query', 'file_path', 'file_type', 'download_status'
        ])
    
    def google_search(self, query, start_index=1, num=10):
        """
        Performs a Google search using the Custom Search JSON API.
        
        Args:
            query (str): The search query
            start_index (int): The index of the first result to return
            num (int): The number of results to return
            
        Returns:
            dict: The search results
        """
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(
            q=query,
            cx=self.cse_id,
            start=start_index,
            num=num
        ).execute()
        
        return res.get('items', [])
    
    def download_file(self, url, category, query):
        """
        Downloads a file from a URL and saves it to the output directory.
        
        Args:
            url (str): The URL of the file to download
            category (str): The category of the search query
            query (str): The search query used to find the file
            
        Returns:
            str: The path to the downloaded file, or None if download failed
        """
        try:
            parsed_url = urlparse(url)
            file_name = os.path.basename(parsed_url.path)
            
            # Clean the filename
            file_name = re.sub(r'[^\w\-\.]', '_', file_name)
            
            # Add a query hash if filename is too generic
            if len(file_name) < 10 or file_name.count('_') > 3:
                query_hash = abs(hash(query)) % 10000
                file_name = f"{query_hash}_{file_name}"
            
            category_dir = os.path.join(self.output_dir, category)
            file_path = os.path.join(category_dir, file_name)
            
            # Check file extension
            file_ext = os.path.splitext(file_name)[1].lower()
            if not file_ext:
                if 'pdf' in url.lower():
                    file_path += '.pdf'
                else:
                    file_path += '.html'
            
            # Download the file
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            
            return file_path
        
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            return None
    
    def extract_domain(self, url):
        """Extracts the domain from a URL."""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain
    
    def scrape(self, max_results_per_query=20):
        """
        Scrapes data for all search queries.
        
        Args:
            max_results_per_query (int): Maximum number of results to fetch per query
            
        Returns:
            pandas.DataFrame: The scraped data
        """
        total_queries = sum(len(queries) for queries in self.search_queries.values())
        query_count = 0
        
        for category, queries in self.search_queries.items():
            for query in queries:
                query_count += 1
                print(f"Processing query {query_count}/{total_queries}: {query}")
                
                # Process results in batches of 10 (Google CSE API limit)
                for start_index in range(1, max_results_per_query + 1, 10):
                    batch_size = min(10, max_results_per_query - start_index + 1)
                    if batch_size <= 0:
                        break
                    
                    try:
                        results = self.google_search(query, start_index, batch_size)
                        
                        for result in results:
                            title = result.get('title', '')
                            link = result.get('link', '')
                            snippet = result.get('snippet', '')
                            source = self.extract_domain(link)
                            
                            # Determine file type
                            file_type = 'html'  # default
                            if 'filetype:pdf' in query or link.lower().endswith('.pdf'):
                                file_type = 'pdf'
                            elif link.lower().endswith(('.doc', '.docx')):
                                file_type = 'doc'
                            
                            # Download the file
                            file_path = None
                            download_status = 'not_attempted'
                            
                            if file_type in ['pdf', 'doc']:
                                try:
                                    file_path = self.download_file(link, category, query)
                                    download_status = 'success' if file_path else 'failed'
                                except Exception as e:
                                    download_status = f'error: {str(e)}'
                            
                            # Add to DataFrame
                            new_row = pd.DataFrame([{
                                'title': title,
                                'link': link,
                                'snippet': snippet,
                                'source': source,
                                'category': category,
                                'query': query,
                                'file_path': file_path,
                                'file_type': file_type,
                                'download_status': download_status
                            }])
                            
                            self.results_df = pd.concat([self.results_df, new_row], ignore_index=True)
                        
                        # Save intermediate results
                        self.save_results()
                        
                        # Pause to avoid rate limiting
                        time.sleep(random.uniform(1.0, 3.0))
                    
                    except Exception as e:
                        print(f"Error processing query '{query}': {str(e)}")
        
        return self.results_df
    
    def save_results(self):
        """Saves the results to a CSV file."""
        csv_path = os.path.join(self.output_dir, 'cbdc_results.csv')
        self.results_df.to_csv(csv_path, index=False)
        
        # Also save as Excel for easier viewing
        excel_path = os.path.join(self.output_dir, 'cbdc_results.xlsx')
        self.results_df.to_excel(excel_path, index=False)
        
        print(f"Results saved to {csv_path} and {excel_path}")
    
    def analyze_results(self):
        """
        Performs basic analysis on the scraped data.
        
        Returns:
            dict: Analysis results
        """
        analysis = {
            'total_results': len(self.results_df),
            'results_by_category': self.results_df['category'].value_counts().to_dict(),
            'results_by_source': self.results_df['source'].value_counts().head(10).to_dict(),
            'download_status': self.results_df['download_status'].value_counts().to_dict(),
            'file_types': self.results_df['file_type'].value_counts().to_dict()
        }
        
        # Save analysis to JSON
        import json
        analysis_path = os.path.join(self.output_dir, 'analysis.json')
        with open(analysis_path, 'w') as f:
            json.dump(analysis, f, indent=4)
        
        return analysis

def main():
    """Main entry point for the scraper."""
    # You'll need to provide your own API key and CSE ID
    API_KEY = "YOUR_GOOGLE_API_KEY"
    CSE_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
    
    scraper = CBDCScraper(API_KEY, CSE_ID)
    results = scraper.scrape(max_results_per_query=30)
    analysis = scraper.analyze_results()
    
    print("\nScraping completed!")
    print(f"Total results: {analysis['total_results']}")
    print("\nResults by category:")
    for category, count in analysis['results_by_category'].items():
        print(f"  {category}: {count}")
    
    print("\nTop sources:")
    for source, count in analysis['results_by_source'].items():
        print(f"  {source}: {count}")

if __name__ == "__main__":
    main()
