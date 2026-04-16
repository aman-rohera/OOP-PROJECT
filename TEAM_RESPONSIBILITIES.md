# Team Responsibilities & Module Ownership

## Team Member: Aman
**Role:** Inventory & Pricing System  
**Responsibilities:** Manage inventory (products, stock), Handle available stock (reserved + faulty items), Implement pricing system, Handle different pricing types (standard, discount, emergency)

### Owned Modules:
- `inventory/` - All inventory management
  - `__init__.py`
  - `inventory_manager.py` - Product stock management
- `pricing/` - All pricing strategies
  - `__init__.py`
  - `pricing_strategy.py` - Abstract pricing interface
  - `standard_pricing.py` - 1.0x multiplier
  - `discounted_pricing.py` - 0.8x multiplier  
  - `emergency_pricing.py` - 1.5x multiplier
- `data/` - Inventory data storage
  - `inventory.json` - Product data persistence
  - `inventory_food.json` - Food kiosk products
  - `inventory_pharmacy.json` - Pharmacy kiosk products
  - `inventory_emergency.json` - Emergency kiosk products

### Key Operations:
- Product CRUD operations
- Price calculations and multipliers
- Stock updates after transactions
- Per-kiosk inventory filtering

---

## Team Member: Vivek
**Role:** Event System & Failure Handling  
**Responsibilities:** Handle event system, Handle different events, Notify other systems, Handle failures step by step (retry-alert)

### Owned Modules:
- `events/` - All event system
  - `__init__.py`
  - `event_system.py` - Event bus infrastructure
  - `events.py` - Event type definitions
  - `subscribers.py` - Subscriber management
- `hardware/` - All failure handling
  - `__init__.py`
  - `failure_handler.py` - Detect & manage failures
  - `retry_handler.py` - Retry logic for failed operations
  - `recalibration_handler.py` - Recalibration on failure
  - `technician_handler.py` - Alert technician (chain of responsibility)
- `data/` - Event logs
  - `transactions.json` - Transaction event logs

### Key Operations:
- Publishing events (TransactionEvent, InventoryUpdateEvent, PricingChangedEvent, etc.)
- Subscribing systems to events
- Failure detection and handling chains
- Event logging and persistence

---

## Team Member: Divyesh
**Role:** Kiosk Core & State Management  
**Responsibilities:** Design main kiosk class, Create KioskInterface, Manage different modes (active, maintenance, emergency, power-saving), Control system behavior

### Owned Modules:
- `core/` - Core kiosk system
  - `__init__.py`
  - `kiosk.py` - Main kiosk entity
  - `kiosk_interface.py` - Facade interface for external access
  - `kiosk_factory.py` - Factory for creating different kiosk types
  - `central_registry.py` - System-wide registry
- `state/` - Kiosk state management
  - `__init__.py`
  - `kiosk_state.py` - Abstract state interface
  - `active_state.py` - Active operational mode
  - `maintenance_state.py` - Maintenance mode
  - `emergency_state.py` - Emergency lockdown mode
  - `power_saving_state.py` - Power-saving mode
- `data/` - Kiosk configuration
  - `config.json` - System configuration

### Key Operations:
- State transitions (Active ↔ Maintenance ↔ Emergency ↔ PowerSaving)
- Mode-specific behavior control
- Kiosk type creation and initialization
- External system interface via Facade pattern

---

## Team Member: Diya
**Role:** Transaction System  
**Responsibilities:** Implement command system, Create commands (purchase, restock, refund), Manage execution and logging of transactions

### Owned Modules:
- `transactions/` - All transaction handling
  - `__init__.py`
  - `command.py` - Abstract command interface
  - `purchase_command.py` - Purchase transaction command
  - `restock_command.py` - Restock transaction command
  - `transaction_memento.py` - Transaction undo/rollback support
- `persistence/` - All data persistence
  - `__init__.py`
  - `data_manager.py` - JSON I/O for all data (inventory, transactions, config)

### Key Operations:
- Command creation and execution
- Purchase transactions with price calculation
- Restock operations
- Transaction undo/rollback via Memento pattern
- Persist all data to JSON files
- Load kiosk-specific inventory on startup

---

## Team Member: (Global Infrastructure)
**GUI & Application Layer** - Shared responsibility (should be assigned to a member)

### Modules:
- `gui/` - User interface
  - `__init__.py`
  - `app.py` - Main user shopping interface
  - `styles.py` - UI styling
  - `admin_dialogs.py` - Admin control panel & dialogs
  - `kiosk_selection.py` - Kiosk type selection screen
- `admin/` - Admin operations
  - `__init__.py`
  - `admin_manager.py` - Admin CRUD operations (uses Aman's inventory, Vivek's events, Diya's persistence)
- `main.py` - Application entry point (orchestrates all modules)

### Key Operations:
- User purchase interface
- Admin management interface
- System initialization and coordination
- Integration of all subsystems

---

## Design Pattern Distribution

| Pattern | Owner(s) | Module |
|---------|----------|--------|
| **Strategy** | Aman | `pricing/` |
| **Observer** | Vivek | `events/` |
| **Chain of Responsibility** | Vivek | `hardware/` |
| **State** | Divyesh | `state/` |
| **Facade** | Divyesh | `core/kiosk_interface.py` |
| **Factory** | Divyesh | `core/kiosk_factory.py` |
| **Command** | Diya | `transactions/command.py` |
| **Memento** | Diya | `transactions/transaction_memento.py` |
| **Singleton** | Divyesh | `core/central_registry.py` |

---

## Inter-Team Dependencies

```
GUI (Presentation Layer)
  ↓
KioskInterface (Divyesh) ← Facade
  ↓
Main Kiosk System (Divyesh) + Pricing (Aman) + Transactions (Diya) + Events (Vivek)
  ↓
Inventory (Aman) + State (Divyesh) + Events (Vivek)
  ↓
Persistence (Diya)
```

- **Aman** manages product data; **Diya** persists it
- **Vivek** publishes events when modules change state; all modules subscribe
- **Diya** executes commands using **Aman's** inventory; publishes via **Vivek's** event bus
- **Divyesh** orchestrates state transitions and provides external API
