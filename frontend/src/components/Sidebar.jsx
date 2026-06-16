/**
 * Sidebar Component
 * Navigation and filtering sidebar for future expansion
 */

export default function Sidebar({ collections = [], selectedCollection = null, onSelectCollection }) {
  return (
    <aside className="sidebar">
      <nav>
        <h3>Collections</h3>
        <ul>
          <li>
            <button 
              className={selectedCollection === null ? "active" : ""}
              onClick={() => onSelectCollection(null)}
            >
              All Prompts
            </button>
          </li>
          {collections.map((collection) => (
            <li key={collection.id}>
              <button
                className={selectedCollection === collection.id ? "active" : ""}
                onClick={() => onSelectCollection(collection.id)}
              >
                {collection.name}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
