/**
 * Header Component
 * Displays the application header and hero section
 */

export default function Header() {
  return (
    <header className="hero">
      <div>
        <p className="eyebrow">PromptLab</p>
        <h1>Prompt Engineering Workspace</h1>
        <p>
          Create, organize, edit, and manage prompts from a React frontend connected to the FastAPI backend.
        </p>
      </div>
    </header>
  );
}
