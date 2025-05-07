import React from 'react';

function Button({label, onClick, color = 'gray' }) {

  const colorClasses = {
    gray: 'bg-gray-800 hover:bg-gray-900 dark:bg-gray-800 dark:hover:bg-gray-700',
    blue: 'bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-500',
    green: 'bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-500',
    red: 'bg-red-500 hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-500',
  };
  return (
      <button 
	  	onClick={onClick}
          className={`text-white focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 ${colorClasses[color]}`}>
        {label}
      </button>
  );
}

export default Button;