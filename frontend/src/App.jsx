import CustomerList from "../components/CustomerList";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-purple-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-white">
                🚀 Think41 Customer Portal
              </h1>
            </div>
            <div className="text-white text-sm">Customer Management System</div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="py-8">
        <CustomerList />
      </main>
    </div>
  );
}

export default App;
