import { useState } from 'react';
import PreData from "../data/predData.json";
import TopGainers from "../data/topGainers.json";
import TopLosers from "../data/topLosers.json";
import './Analysis.css';

const CombinedAnalysis = () => {
  const [selectedCrop, setSelectedCrop] = useState(null);

  // Function to get price change class
  const getPriceChangeClass = (change) => {
    const numChange = parseFloat(change);
    return numChange > 0 ? 'positive-change' : numChange < 0 ? 'negative-change' : numChange === 0 ? 'no-change' : '';
  };

  // Function to get crop details
  const getCropDetails = (cropName) => {
    return PreData.filter(item => item.Crop === cropName);
  };

  return (
    <div className="container">
      <h1 className="dashboard-title">Market Analysis Dashboard</h1>
      
      {/* Top Gainers and Losers Section */}
      <div className="analysis-grid">
        {/* Top Gainers */}
        <div className="analysis-card">
          <h1 className="section-title gainers-title">Top Gainers</h1>
          <table className="analysis-table">
            <thead>
              <tr>
                <th>Crop</th>
                <th className="text-center">Price</th>
                <th className="text-center">Change</th>
              </tr>
            </thead>
            <tbody>
              {TopGainers.map((item, index) => (
                <tr key={index}>
                  <td>{item.Crop}</td>
                  <td className="text-center">{item.Price}</td>
                  <td className={`text-center ${getPriceChangeClass(item.Change)}`}>
                    {item.Change}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Top Losers */}
        <div className="analysis-card">
          <h1 className="section-title losers-title">Top Losers</h1>
          <table className="analysis-table">
            <thead>
              <tr>
                <th>Crop</th>
                <th className="text-center">Price</th>
                <th className="text-center">Change</th>
              </tr>
            </thead>
            <tbody>
              {TopLosers.map((item, index) => (
                <tr key={index}>
                  <td>{item.Crop}</td>
                  <td className="text-center">{item.Price}</td>
                  <td className={`text-center ${getPriceChangeClass(item.Change)}`}>
                    {item.Change}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Crop Grid */}
      <div>
        <h2 className="section-title">All Crops Analysis</h2>
        <div className="crops-grid">
          {[...new Set(PreData.map(item => item.Crop))].map((crop, index) => (
            <div 
              key={index}
              className="crop-card"
              onClick={() => setSelectedCrop(crop)}
            >
              <h3>{crop}</h3>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Crop Details */}
      {selectedCrop && (
        <div className="analysis-card crop-details">
          <h2 className="section-title">Details for {selectedCrop}</h2>
          <table className="analysis-table">
            <thead>
              <tr>
                <th>Year</th>
                <th>Month</th>
                <th className="text-center">Average Price (₹)</th>
                <th className="text-center">Price Change</th>
              </tr>
            </thead>
            <tbody>
              {getCropDetails(selectedCrop).map((item) => 
                item.Data.map((data, idx) => (
                  <tr key={`${item.Year}-${idx}`}>
                    <td>{item.Year}</td>
                    <td>{data.Month}</td>
                    <td className="text-center">₹{data.AveragePrice}</td>
                    <td className={`text-center ${getPriceChangeClass(data.PriceChangeIndicator)}`}>
                      {data.PriceChangeIndicator}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CombinedAnalysis;