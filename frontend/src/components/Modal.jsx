/**
 * Modal Component
 * Reusable modal/dialog component for confirmations and alerts
 */

import Button from "./Button";

export default function Modal({ 
  isOpen, 
  title, 
  message, 
  onConfirm, 
  onCancel,
  confirmText = "Confirm",
  cancelText = "Cancel",
  isDanger = false
}) {
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>{title}</h3>
        <p>{message}</p>
        <div className="modal-actions">
          <Button 
            variant={isDanger ? "danger" : "primary"} 
            onClick={onConfirm}
          >
            {confirmText}
          </Button>
          <Button 
            variant="secondary" 
            onClick={onCancel}
          >
            {cancelText}
          </Button>
        </div>
      </div>
    </div>
  );
}
