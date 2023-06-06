import axios from 'axios';
import { STOCK_API_URL } from '../App';
export default class StockProvider {
    static STOCK_API_URL = process.env.REACT_APP_STOCK_API_URL;

    static parseToNumber(number) {
      if (number === null || isNaN(number)) {
        return 'N/A';
      } else {
        return number.toFixed(2);
      }
    }
    static parseDates = (stockHistory) => {
      stockHistory = stockHistory.map((element) => {
        element.date = new Date(element.date.$date).toLocaleDateString();
        return element;
      });
      return stockHistory;
    }
    static async getStocks() {
        const stocks = axios
                .get(this.STOCK_API_URL)
                .then((res) => {
                    let stocks = res.data;
                    stocks = stocks.map((stock) => { 
                        stock.price = this.parseToNumber(stock.price);
                        stock.change = this.parseToNumber(stock.change);
                        stock.change_percent = this.parseToNumber(stock.change_percent);
                        stock.previous_close = this.parseToNumber(stock.previous_close);
                        stock.open_price = this.parseToNumber(stock.open_price);
                        stock.volume = (stock.volume === null || stock.volume === '') ? 'N/A' : stock.volume;
                        console.log(stock);
                        return stock;
                    });
                    return stocks
                })
                .catch((err) => {
                    console.log(err);
                    return [];
                })
        return stocks;
    }

    static async getStock(ticker) {
        const stock = axios
                .get(this.STOCK_API_URL+ticker)
                .then((res) => {
                    let stock = res.data;
                    stock.price = this.parseToNumber(stock.price);
                    stock.change = this.parseToNumber(stock.change);
                    stock.change_percent = this.parseToNumber(stock.change_percent);
                    stock.previous_close = this.parseToNumber(stock.previous_close);
                    stock.open_price = this.parseToNumber(stock.open_price);
                    stock.volume = (stock.volume === null || stock.volume === '') ? 'N/A' : stock.volume;
                    stock.stock_history = this.parseDates(stock.stock_history);
                    return stock;
                })
                .catch((err) => {
                    return null;
                });
        return stock;
    }
}