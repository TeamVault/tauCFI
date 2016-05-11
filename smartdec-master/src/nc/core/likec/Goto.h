/* * SmartDec decompiler - SmartDec is a native code to C/C++ decompiler
 * Copyright (C) 2015 Alexander Chernov, Katerina Troshina, Yegor Derevenets,
 * Alexander Fokin, Sergey Levin, Leonid Tsvetkov
 *
 * This file is part of SmartDec decompiler.
 *
 * SmartDec decompiler is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SmartDec decompiler is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SmartDec decompiler.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#include <nc/config.h>

#include <memory>

#include "Expression.h"
#include "Statement.h"

namespace nc {
namespace core {
namespace likec {

/**
 * Goto statement.
 */
class Goto: public Statement {
    std::unique_ptr<Expression> destination_; ///< Goto destination address.

    public:

    /**
     * Class constructor.
     *
     * \param[in] tree Owning tree.
     * \param[in] destination Goto destination address.
     */
    Goto(Tree &tree, std::unique_ptr<Expression> destination):
        Statement(tree, GOTO), destination_(std::move(destination)) {}

    /**
     * \return Goto destination address.
     */
    Expression *destination() { return destination_.get(); }

    /**
     * \return Goto destination address.
     */
    const Expression *destination() const { return destination_.get(); }

    virtual void visitChildNodes(Visitor<TreeNode> &visitor) override;

    virtual Goto *rewrite() override;

    protected:

    virtual void doPrint(PrintContext &context) const override;
};

} // namespace likec
} // namespace core
} // namespace nc

NC_REGISTER_CLASS_KIND(nc::core::likec::Statement, nc::core::likec::Goto, nc::core::likec::Statement::GOTO)

/* vim:set et sts=4 sw=4: */
