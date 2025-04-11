import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders Mergify Title text', () => {
  render(<App />);
  const linkElement = screen.getByText(/Mergify/i);
  expect(linkElement).toBeInTheDocument();
});
