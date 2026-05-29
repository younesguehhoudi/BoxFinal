
# UI — Technical Documentation (CLI)

**Authors:** Abdallah Alamoush · Younes Guehhoudi · Noé Loisel

---

## Purpose & Scope

This document describes the technical design and responsibilities of the Command Line Interface (CLI) UI only. It focuses on the `Ui/` folder and the UI-facing behavior of `main.py` / `ConsoleMenu.py`. It does not document business logic or database internals beyond the UI's visible interactions.

## High-level responsibilities

- Present menus, prompts, and formatted results to the terminal.
- Validate and sanitize user input before invoking business logic.
- Maintain session state (current authenticated user) and enforce access control for protected actions.
- Route user choices to UI handlers and present results returned by the Logic layer.
- Translate errors and exceptions into clear, actionable messages for users.

## Module responsibilities

- `Ui/ConsoleMenu.py`: main loop, menu rendering, selection routing, and session holder (`current_user`).
- `Ui/Login.py`: login and account-creation prompts and flows; updates session state on success.
- `Ui/PlacePrinter.py`: formatting and printing places (lists and single entries).
- `Ui/TourPrinter.py`: formatting and printing tours, distance summaries, and route steps.
- `Ui/TourSharingPrinter.py`: display view for shared tours (read-only, token-based).
- Any UI helpers: input parsing, confirmation prompts, common text/styles (colors, separators).

## UI → Logic contract (expected call patterns)

UI treats Logic as a synchronous service layer. Example expected interfaces (thin adapter allowed):

- `Auth.login(username: str, password: str) -> User` or raises `AuthError` on failure
- `Auth.create_user(username: str, password: str) -> User`
- `Place.add_place(user_id: int, name: str) -> Place`
- `Place.list_user_places(user_id: int) -> List[Place]`
- `Algo.generate_tour(place_ids: List[int]) -> TourData` (may raise `GenerationError`)
- `HotelPlanner.plan_hotels(coords: List[Coord]) -> List[HotelSuggestion]`
- `TourManager.save_tour(user_id: int, name: str, tour_data, visibility: str) -> Tour`
- `TourManager.list_public_tours() -> List[TourSummary]`
- `TourManager.get_tour_by_token(token: str) -> Tour`

Contract rules:

- UI callers must handle return values and expected exceptions; Logic should use explicit exceptions or error objects, not print to stdout.
- Keep calls short and synchronous from the UI point of view; long-running tasks should report progress or offer to run asynchronously.

## Typical state & data flow (example: generate → save tour)

1. User selects option `4` in `ConsoleMenu.py`.
2. UI shows saved places via `Place.list_user_places()` and `PlacePrinter.print_places()`; user selects indices → `place_ids`.
3. UI calls `Algo.generate_tour(place_ids)`.
	- On failure: show friendly error, allow retry or return to main menu.
4. UI displays optimized route via `TourPrinter.print_tour()` including `total_distance`.
5. Optionally call `HotelPlanner.plan_hotels()` and display suggestions.
6. If user chooses to save, collect `name` and `visibility`, call `TourManager.save_tour()` and display confirmation and share token if relevant.

## Input validation & error handling

- Validate locally before calling Logic: menu range, integer indices within bounds, non-empty strings, reasonable length limits (e.g., name ≤ 100 chars).
- Treat external IO (geocoding, network) as fallible: show short error + retry/cancel.
- Auth-guard protected commands must check `current_user` early and redirect to login flow if absent.
- Present errors succinctly (headline + action). Log full details to a debug log (separate from user output).

## Presentation & formatting guidelines

- Printers expose a small API (e.g., `print_places(places)`, `print_tour(tour)`); UI handlers call printers instead of inlining formatting.
- Distances in kilometers with one decimal place; coordinates with 4–6 decimal places.
- Use indices for selection lists and consistent separators for readability.
- Confirmation prompts use explicit `y/n` with defaults shown.

## Session & authentication lifecycle

- `ConsoleMenu.py` holds an in-memory `current_user` (or `None`).
- Login flow sets `current_user` and updates menu header to show username.
- Logout clears `current_user` and any UI-local caches.
- Protected actions check `current_user` before invoking Logic.

## Menu routing (canonical mapping)

- `1` — Login / Create / Logout → `Ui/Login.py` → `Auth`
- `2` — Add place → prompt name → `Place.add_place`
- `3` — Show my places → `Place.list_user_places` → `PlacePrinter`
- `4` — Generate / save tour → `Algo` + `HotelPlanner` + `TourManager` → `TourPrinter`
- `5` — Show public tours → `TourManager.list_public_tours` → `TourPrinter`
- `6` — My saved tours → `TourManager.list_user_tours` → `TourPrinter`
- `7` — Access shared tour → prompt token → `TourManager.get_tour_by_token` → `TourSharingPrinter`
- `8` — Quit → graceful shutdown

## Testing guidance (UI-focused)

- Unit tests: mock Logic layer and simulate stdin/stdout to verify routing and error handling. Place UI tests under `Test/Ui/` or reuse `Test/Logic/` with mocks.
- Printer tests: snapshot text output for sample objects to assert stable formatting.
- Integration tests: use a temporary/in-memory SQLite DB and scripted stdin to validate end-to-end flows.
- Error tests: simulate geocoding failures, DB errors, invalid tokens to ensure graceful UI recovery.

## Extension points & best practices

- Keep formatting in printers so UI handlers remain thin.
- Centralize menu→handler mapping for easier extension.
- Provide an adapter layer if Logic APIs change, instead of modifying many UI handlers.
- Add non-intrusive debug logging for troubleshooting; avoid exposing logs to regular users.

## Developer checklist

- Verify auth guard for protected actions.
- Use the appropriate printer module for output.
- Catch exceptions from Logic and present user-friendly messages.
- Keep business logic out of UI modules; orchestrate only.
- Add tests for new UI behaviors.

---

If you want, I can now:

- generate a one-page ASCII sequence diagram for the login or generate-tour flow, or
- add a starter UI test `Test/Ui/TestConsoleMenu.py` that mocks the Logic layer. 

Tell me which and I'll add it to the repo.
