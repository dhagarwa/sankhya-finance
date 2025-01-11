import asyncio
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, date
from stock_analyst_agent import StockAnalystAgent
import os
import sys

class WebsiteGenerator:
    def __init__(self):
        self.root_dir = Path("website")
        
    def _check_dependencies(self):
        """Check if required dependencies are installed"""
        try:
            # Check for Node.js
            node_version = subprocess.run(['node', '-v'], capture_output=True, text=True)
            if node_version.returncode != 0:
                print("Node.js is not installed. Please install from: https://nodejs.org/")
                sys.exit(1)
                
            # Check for npm
            npm_version = subprocess.run(['npm', '-v'], capture_output=True, text=True)
            if npm_version.returncode != 0:
                print("npm is not installed. Please install Node.js which includes npm")
                sys.exit(1)
                
            print(f"✓ Node.js version: {node_version.stdout.strip()}")
            print(f"✓ npm version: {npm_version.stdout.strip()}")
            
        except FileNotFoundError:
            print("""
Error: Required dependencies not found.
Please install:
1. Node.js (includes npm): https://nodejs.org/
2. After installation, restart your terminal and run this script again
            """)
            sys.exit(1)
            
    def _create_astro_project(self):
        """Create new Astro project with TypeScript"""
        print("\nCreating new Astro project...")
        if self.root_dir.exists():
            shutil.rmtree(self.root_dir)
            
        try:
            # Use subprocess for better error handling
            subprocess.run([
                'npm', 'create', 'astro@latest', str(self.root_dir),
                '--', '--template', 'basics', '--typescript', '--install', '--no-git'
            ], check=True)
            
            subprocess.run([
                'npm', 'install', '@astrojs/tailwind', '@astrojs/react', 'framer-motion'
            ], cwd=str(self.root_dir), check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"Error creating Astro project: {e}")
            sys.exit(1)
    
    def _create_component_files(self):
        """Create React components"""
        components_dir = self.root_dir / "src/components"
        components_dir.mkdir(exist_ok=True)
        
        # Create StockTable component
        stock_table = '''
import { motion } from "framer-motion";
import type { StockRecommendation } from '../types';

interface Props {
    recommendations: StockRecommendation[];
}

export default function StockTable({ recommendations }: Props) {
    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: { staggerChildren: 0.1 }
        }
    };

    const item = {
        hidden: { y: 20, opacity: 0 },
        show: { y: 0, opacity: 1 }
    };

    return (
        <motion.div
            variants={container}
            initial="hidden"
            animate="show"
            className="overflow-hidden rounded-xl bg-white/10 backdrop-blur-lg"
        >
            <table className="w-full">
                <thead>
                    <tr className="bg-purple-900/50">
                        <th className="p-4 text-left text-purple-100">Ticker</th>
                        <th className="p-4 text-left text-purple-100">Signal</th>
                        <th className="p-4 text-left text-purple-100">Confidence</th>
                        <th className="p-4 text-left text-purple-100">Analysis</th>
                    </tr>
                </thead>
                <tbody>
                    {recommendations.map((stock, index) => (
                        <motion.tr
                            key={stock.ticker}
                            variants={item}
                            className="border-t border-purple-800/30"
                        >
                            <td className="p-4 font-mono">{stock.ticker}</td>
                            <td className={`p-4 font-semibold ${
                                stock.recommendation === "BUY" ? "text-green-400" :
                                stock.recommendation === "SELL" ? "text-red-400" :
                                "text-yellow-400"
                            }`}>
                                {stock.recommendation}
                            </td>
                            <td className="p-4">{(stock.confidence * 100).toFixed(1)}%</td>
                            <td className="p-4 text-gray-300">{stock.rationale}</td>
                        </motion.tr>
                    ))}
                </tbody>
            </table>
        </motion.div>
    );
}'''
        
        disclaimer = '''
export default function Disclaimer() {
    return (
        <div className="rounded-xl bg-white/5 backdrop-blur-md p-6 border border-white/10">
            <p className="text-purple-200">
                ⚠️ The recommendations provided by Sankhya AI are for educational purposes only.
                Always conduct your own research and consult with a qualified financial advisor.
            </p>
        </div>
    );
}'''

        (components_dir / "StockTable.tsx").write_text(stock_table)
        (components_dir / "Disclaimer.tsx").write_text(disclaimer)

    async def generate_website(self):
        """Generate Astro website with data"""
        print("\nGenerating Sankhya AI website...")
        
        # Check dependencies first
        self._check_dependencies()
        
        # Create Astro project
        self._create_astro_project()
        
        # Create components
        self._create_component_files()
        
        # Get recommendations data
        analyst = StockAnalystAgent()
        recommendations_df = await analyst.analyze_sp500()
        
        # Save recommendations data
        data = recommendations_df.to_dict('records')
        data_dir = self.root_dir / "src/data"
        data_dir.mkdir(exist_ok=True)
        
        # Convert date objects to string format
        def serialize_data(data):
            # Iterate over each item in the list
            for item in data:
                # Serialize each item (which is a dictionary)
                for key, value in item.items():
                    if isinstance(value, date):
                        item[key] = value.isoformat()  # Convert date to string
            return data  # Return the modified list
        
        with open(data_dir / "recommendations.json", "w") as f:
            json.dump(serialize_data(data), f, indent=2)
        
        print(f"\nWebsite generated successfully at: {self.root_dir.absolute()}")
        print("To start development server:")
        print(f"cd {self.root_dir} && npm run dev")

if __name__ == "__main__":
    generator = WebsiteGenerator()
    asyncio.run(generator.generate_website())