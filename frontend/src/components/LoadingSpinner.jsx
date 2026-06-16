/**
 * LoadingSpinner Component
 * Displays a loading indicator
 */

export default function LoadingSpinner({ isLoading = false, message = "Loading..." }) {
  if (!isLoading) return null;
  
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <p>{message}</p>
    </div>
  );
}
