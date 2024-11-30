// Form to add a new expense
import { useState } from 'react';
import axios from 'axios';

const ExpenseForm = ({ onExpenseAdded }) => {
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    try {
      await axios.post(
        'http://localhost:8000/expenses/',
        { category, amount, description },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      onExpenseAdded(); // Refresh the expense list
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h3>Add New Expense</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Category</label>
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <button type="submit">Add Expense</button>
      </form>
    </div>
  );
};

export default ExpenseForm;
