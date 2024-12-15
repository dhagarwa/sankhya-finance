import { motion } from "framer-motion";
import type { StockRecommendation } from '../types';
import { useState, useEffect } from 'react';

interface Props {
    recommendations: StockRecommendation[];
}

export default function StockTable({ recommendations = [] }: Props) {
    const [searchQuery, setSearchQuery] = useState('');
    const [filteredRecommendations, setFilteredRecommendations] = useState(recommendations);

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

    useEffect(() => {
        console.log('Recommendations:', recommendations);
        console.log('Filtered:', filteredRecommendations);
        const filtered = recommendations.filter(stock =>
            stock.ticker.toLowerCase().includes(searchQuery.toLowerCase().trim())
        );
        setFilteredRecommendations(filtered);
    }, [searchQuery, recommendations]);

    return (
        <div className="p-8 max-w-7xl mx-auto">
            <div className="relative">
                <div className="absolute -inset-2 bg-gradient-to-r from-purple-600/20 via-pink-500/20 to-blue-600/20 rounded-3xl blur-3xl" />
                
                <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-900/95 to-gray-900/90 backdrop-blur-xl border border-purple-500/20 shadow-2xl">
                    <div className="px-8 py-6 border-b border-purple-500/20">
                        <div className="flex flex-col space-y-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h2 className="text-3xl font-bold text-white">
                                        Sankhya Finance
                                    </h2>
                                    <p className="text-purple-200 mt-1">
                                        AI-Powered Stock Analyst
                                    </p>
                                </div>
                                <div className="relative">
                                    <input
                                        type="text"
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        placeholder="Search ticker..."
                                        className="w-64 px-4 py-2 rounded-xl bg-purple-900/30 border border-purple-500/30 
                                                 text-purple-100 placeholder-purple-400/50 focus:outline-none 
                                                 focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 
                                                 transition-all duration-200"
                                    />
                                    <span className="absolute right-3 top-1/2 -translate-y-1/2 text-purple-400/50">
                                        🔍
                                    </span>
                                </div>
                            </div>
                            <div className="text-sm text-purple-300/80 bg-purple-900/20 px-4 py-2 rounded-lg">
                                ⚠️ Disclaimer: The recommendations provided are for informational purposes only. 
                                Always conduct your own research and consult with a qualified financial advisor before making investment decisions.
                            </div>
                        </div>
                    </div>
                    
                    <motion.div
                        variants={container}
                        initial="hidden"
                        animate="show"
                        className="overflow-x-auto"
                    >
                        <table className="w-full">
                            <thead>
                                <tr className="bg-gradient-to-r from-purple-900/50 via-purple-800/50 to-purple-900/50">
                                    <th className="px-8 py-5 text-left text-sm font-medium text-purple-200 uppercase tracking-wider">
                                        Ticker
                                    </th>
                                    <th className="px-8 py-5 text-left text-sm font-medium text-purple-200 uppercase tracking-wider">
                                        Signal
                                    </th>
                                    <th className="px-8 py-5 text-left text-sm font-medium text-purple-200 uppercase tracking-wider">
                                        Analysis
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-purple-800/30">
                                {filteredRecommendations.map((stock) => (
                                    <motion.tr
                                        key={stock.ticker}
                                        variants={item}
                                        className="hover:bg-purple-900/30 transition-all duration-200 ease-in-out backdrop-blur-lg group"
                                    >
                                        <td className="px-8 py-6">
                                            <div className="flex items-center space-x-3">
                                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center border border-purple-500/30 group-hover:border-purple-500/50 transition-colors">
                                                    <span className="font-mono text-lg font-bold bg-gradient-to-r from-purple-200 to-pink-200 bg-clip-text text-transparent">
                                                        {stock.ticker.slice(0, 2)}
                                                    </span>
                                                </div>
                                                <span className="font-mono text-lg font-semibold text-purple-100">
                                                    {stock.ticker}
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-8 py-6">
                                            <span className={`inline-flex items-center px-4 py-2 rounded-xl text-sm font-medium shadow-lg ${
                                                stock.recommendation === "BUY" 
                                                    ? "bg-green-500/10 text-green-400 border border-green-500/30 shadow-green-500/20" :
                                                stock.recommendation === "SELL" 
                                                    ? "bg-red-500/10 text-red-400 border border-red-500/30 shadow-red-500/20" :
                                                    "bg-yellow-500/10 text-yellow-400 border border-yellow-500/30 shadow-yellow-500/20"
                                            }`}>
                                                {stock.recommendation}
                                            </span>
                                        </td>
                                        <td className="px-8 py-6 text-gray-300">{stock.rationale}</td>
                                    </motion.tr>
                                ))}
                            </tbody>
                        </table>
                    </motion.div>
                </div>
            </div>
        </div>
    );
}