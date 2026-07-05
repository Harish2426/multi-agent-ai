import ApiStatus from "./ApiStatus";

function Sidebar({
  conversationId,
  onNewChat,
  onDelete,
  disabled,
}) {
  return (
    <aside className="sidebar">
      <div>
        <div className="sidebar__brand">
          <span className="sidebar__logo">MA</span>

          <div>
            <strong>Multi-Agent AI</strong>
            <small>Agent workspace</small>
          </div>
        </div>

        <button
          className="sidebar__primary-button"
          type="button"
          onClick={onNewChat}
          disabled={disabled}
        >
          + New chat
        </button>

        <div className="conversation-card">
          <span>Current conversation</span>

          <code>
            {conversationId
              ? `${conversationId.slice(0, 8)}...`
              : "Not started"}
          </code>
        </div>
      </div>

      <div className="sidebar__footer">
        <ApiStatus />

        <button
          className="sidebar__delete-button"
          type="button"
          onClick={onDelete}
          disabled={!conversationId || disabled}
        >
          Delete conversation
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;