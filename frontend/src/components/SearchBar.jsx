/**
 * SearchBar Component
 * Provides search/filter functionality
 */

export default function SearchBar({ 
  value, 
  onChange, 
  placeholder = "Search prompts...",
  className = ""
}) {
  return (
    <input
      type="text"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className={`search-bar ${className}`.trim()}
    />
  );
}
