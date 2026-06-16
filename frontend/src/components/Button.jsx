/**
 * Button Component
 * Reusable button component with multiple variants
 */

export default function Button({ 
  children, 
  type = "button", 
  variant = "primary", 
  onClick, 
  disabled = false,
  className = "",
  ...props 
}) {
  const buttonClass = `${variant} ${className}`.trim();
  
  return (
    <button 
      type={type} 
      className={buttonClass}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
