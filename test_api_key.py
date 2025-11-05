#!/usr/bin/env python3
"""
Test FRED API Key
快速测试您的FRED API密钥是否有效
"""

import sys
import requests

def test_api_key(api_key):
    """Test if FRED API key is valid"""
    print("=" * 60)
    print("Testing FRED API Key...")
    print("=" * 60)

    # Test endpoint
    url = "https://api.stlouisfed.org/fred/series"
    params = {
        'series_id': 'WTREGEN',
        'api_key': api_key,
        'file_type': 'json'
    }

    try:
        print(f"\nAPI Key: {api_key[:10]}...")
        print("Sending test request...\n")

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print("✓ SUCCESS! API key is valid")
            print("\nSeries Info:")
            if 'seriess' in data and len(data['seriess']) > 0:
                series = data['seriess'][0]
                print(f"  ID: {series.get('id', 'N/A')}")
                print(f"  Title: {series.get('title', 'N/A')}")
                print(f"  Frequency: {series.get('frequency', 'N/A')}")
                print(f"  Units: {series.get('units', 'N/A')}")

            # Now test fetching actual data
            print("\nTesting data fetch...")
            data_url = "https://api.stlouisfed.org/fred/series/observations"
            data_params = {
                'series_id': 'WTREGEN',
                'api_key': api_key,
                'file_type': 'json',
                'limit': 5,
                'sort_order': 'desc'
            }

            data_response = requests.get(data_url, params=data_params, timeout=10)
            if data_response.status_code == 200:
                obs_data = data_response.json()
                if 'observations' in obs_data:
                    print("✓ Data fetch successful!")
                    print(f"  Latest observations ({len(obs_data['observations'])} records):")
                    for obs in obs_data['observations'][:5]:
                        print(f"    {obs['date']}: {obs['value']}")

                    print("\n" + "=" * 60)
                    print("✓ Your API key is working perfectly!")
                    print("You can now run the main script:")
                    print(f"  python fetch_shutdown_data_final.py {api_key}")
                    print("=" * 60)
                    return True
            else:
                print(f"✗ Data fetch failed: {data_response.status_code}")
                return False

        elif response.status_code == 400:
            print("✗ ERROR: Bad request")
            print("Your API key format might be incorrect")
            print(f"Response: {response.text}")
            return False

        elif response.status_code == 403:
            print("✗ ERROR: Access denied")
            print("Your API key is invalid or expired")
            print("\nPlease:")
            print("1. Check if you copied the entire key")
            print("2. Get a new key at: https://fred.stlouisfed.org/docs/api/api_key.html")
            return False

        else:
            print(f"✗ ERROR: Unexpected status code {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("✗ ERROR: Request timeout")
        print("Please check your internet connection")
        return False

    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Connection failed")
        print("Please check your internet connection")
        return False

    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("FRED API Key Test Tool")
        print("测试您的FRED API密钥")
        print("=" * 60)
        print("\nUsage:")
        print(f"  python {sys.argv[0]} YOUR_API_KEY")
        print("\nExample:")
        print(f"  python {sys.argv[0]} a1b2c3d4e5f6789012345678901234")
        print("\nDon't have an API key?")
        print("Get one free at: https://fred.stlouisfed.org/docs/api/api_key.html")
        sys.exit(1)

    api_key = sys.argv[1]
    success = test_api_key(api_key)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
