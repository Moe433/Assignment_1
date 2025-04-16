import pandas as pd
<<<<<<< Updated upstream
from sklearn.preprocessing import MinMaxScaler

def engineer_features(df):
    """Adds cybersecurity-specific features with column safety checks"""
    
    # Create copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # 1. Time-based features (always available)
    df['packets_per_second'] = (df['spkts'] + df['dpkts']) / (df['dur'].replace(0, 0.001) + 0.001)
    df['bytes_per_packet'] = (df['sbytes'] + df['dbytes']) / (df['spkts'] + df['dpkts'] + 1)
    
    # 2. Protocol-specific features (conditional)
    if all(col in df.columns for col in ['ct_http', 'ct_flw_http_mthd']):
        df['http_ratio'] = df['ct_http'] / (df['ct_flw_http_mthd'] + 1)
    else:
        print("⚠️  HTTP features not available - skipping")
    
    # 3. Behavioral features (conditional)
    if 'srcip' in df.columns:
        df['srcip_freq'] = df.groupby('srcip')['srcip'].transform('count')
    else:
        print("⚠️  srcip column not available - skipping")
    
    # 4. Normalize numerical features
    num_cols = ['dur', 'sbytes', 'dbytes', 'packets_per_second', 'bytes_per_packet']
    num_cols = [col for col in num_cols if col in df.columns]  # Filter available columns
    
    if num_cols:
        scaler = MinMaxScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])
    else:
        scaler = None
        print("⚠️  No numerical features available for scaling")
    
    return df, scaler

if __name__ == "__main__":
    try:
        # Load your cleaned data
        input_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_combined_cleaned.csv"
        output_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_engineered.csv"
        
        print("🔧 Starting feature engineering...")
        df = pd.read_csv(input_path)
        
        # Engineer features
        engineered_df, scaler = engineer_features(df)
        
        # Save results
        engineered_df.to_csv(output_path, index=False)
        print(f"✅ Saved engineered features to {output_path}")
        print("\nNew features added:")
        print([col for col in engineered_df.columns if col not in df.columns])
        
    except Exception as e:
        print(f"❌ Error during feature engineering: {str(e)}")
=======
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler

def engineer_minimal_features(df):
    df = df.copy()
    
    # Protocol features
    if 'proto' in df.columns:
        df['proto_freq'] = df.groupby('proto')['proto'].transform('count')
        df['is_rare_proto'] = (df['proto_freq'] < 10).astype(int)
    
    # Service features
    if 'service' in df.columns:
        df['service_freq'] = df.groupby('service')['service'].transform('count')
        df['is_unknown_service'] = (df['service'] == 'unknown').astype(int)
    
    # Duration features
    if 'dur' in df.columns:
        df['dur_log'] = np.log1p(df['dur'])
        df['is_long_conn'] = (df['dur'] > 60).astype(int)
    
    # State features
    if 'state' in df.columns:
        df['is_rejected'] = (df['state'] == 'REJ').astype(int)
        df['is_reset'] = (df['state'].str.contains('RST', na=False)).astype(int)
    
    # Normalization
    num_cols = [col for col in ['dur', 'dur_log', 'proto_freq', 'service_freq'] 
               if col in df.columns]
    if num_cols:
        scaler = MinMaxScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])
    
    return df

if __name__ == "__main__":
    try:
        # 1. Define ABSOLUTE paths (recommended)
        input_dir = "/Users/mohammedqudaih/Assignment_1/archive/"
        output_dir = "/Users/mohammedqudaih/Assignment_1/archive/"
        
        input_path = os.path.join(input_dir, "UNSW_NB15_combined_cleaned.csv")
        output_path = os.path.join(output_dir, "UNSW_NB15_engineered_minimal.csv")
        
        # 2. Verify file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found at: {input_path}")
        
        print(f"🔍 Loading data from: {input_path}")
        df = pd.read_csv(input_path)
        
        # 3. Engineer features
        print("⚙️ Engineering features...")
        engineered_df = engineer_minimal_features(df)
        
        # 4. Save output
        engineered_df.to_csv(output_path, index=False)
        print(f"✅ Saved to: {output_path}")
        print("\nNew features:", [col for col in engineered_df.columns if col not in df.columns])
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nDebug Tips:")
        print("- Verify the file exists at the specified path")
        print("- Check file permissions (try `ls -l {input_path}`)")
        print("- If using Jupyter, check your working directory with `!pwd`")
>>>>>>> Stashed changes
