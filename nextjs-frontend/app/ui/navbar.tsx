"use client"

import { useState } from 'react';

export default function NavBar() {
  const [isDropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setDropdownOpen(!isDropdownOpen);
  };

  return (
    <nav className="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-black dark:border-gray-600">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        {/* Home Button on the left side */}
        <button className="text-black dark:text-white font-medium rounded-lg text-sm px-4 py-2 focus:outline-none">
          Home
        </button>

        {/* Account Button with Dropdown on the right */}
        <div className="relative">
          <button
            onClick={toggleDropdown}
            type="button"
            className="text-black dark:text-white font-medium rounded-lg text-sm px-4 py-2 bg-gray-100 dark:bg-gray-700 border border-black dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-gray-500"
          >
            Account
          </button>
          {isDropdownOpen && (
            <div className="absolute right-0 w-48 py-2 mt-2 bg-white dark:bg-gray-800 border border-black dark:border-gray-600 rounded shadow-xl">
              <a href="#" className="block px-4 py-2 text-sm text-black dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Upload File</a>
              <a href="#" className="block px-4 py-2 text-sm text-black dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Settings</a>
              <a href="#" className="block px-4 py-2 text-sm text-black dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">Logout</a>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
