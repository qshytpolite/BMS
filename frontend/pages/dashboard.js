// This page will fetch and display the user's expenses.
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import ExpenseList from '../components/ExpenseList';

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
      return;
    }

    const fetchExpenses = async () => {
      try {
        const response = await axios.get('http://localhost:8000/expenses/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setExpenses(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchExpenses();
  }, [router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Expense Dashboard</h2>
      <ExpenseList expenses={expenses} />
    </div>
  );
};

export default Dashboard;
