/**
 * Layout Component
 * Main application layout wrapper
 */

import Header from "./Header";
import ErrorMessage from "./ErrorMessage";

export default function Layout({ message, error, children }) {
  return (
    <div className="app">
      <Header />
      {message && <div className="alert success">{message}</div>}
      {error && <ErrorMessage message={error} />}
      {children}
    </div>
  );
}
